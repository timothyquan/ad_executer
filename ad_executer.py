__author__ = "Tim Quan"
__copyright__ = "Copyright 2020"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Tim Quan"
__status__ = "Production"

import pandas as pd
import subprocess

from pyad import adcontainer
from threading import Thread
from pprint import pprint
from time import sleep
import socket

def compname_from_dn(computer):
    '''Accepts a computer DN (distinguished name) string
    Returns the fdqn as a string'''
    strings = {}    
    for string in computer.split(','):
        if string[:string.find('=')] in strings.keys():
            strings[string[:string.find('=')]] = strings[string[:string.find('=')]]+'.'+string[string.find('=')+1:]            
        else: 
            strings[string[:string.find('=')]] = string[string.find('=')+1:]
    return f"{strings['CN']}.{strings['DC']}"

def is_online(host, results, idx):
    '''Accepts an IP address or host name, a list of results, and the index for the results to be used
    Returns True if it responds to pings False if not'''

    try: output = str(subprocess.check_output(f'ping {host}'))
    except: output = 'Destination host unreachable.'
    results[idx] = 'Destination host unreachable.'  not in output \
         and f'100 {chr(37)} loss' not in output

def generate_host_list(dn):
    '''Accepts a DN (distinguished name) for an OU containing computers
    Returns the a pandas dataframe with key 'fdqn', 'online' '''
    computers = pd.DataFrame(columns=['fdqn','ip_address','online'])
    threads = []
    ping_results = []

    try: ou = adcontainer.ADContainer.from_dn(dn)
    except: return computers #return empty dataframe in the instance that the dn lookup generated an exception
    for idx, child in enumerate(ou.get_children()):
        ping_results.append(False)
        fdqn = compname_from_dn(child.dn)
        computers.loc[idx] = {'fdqn' : fdqn, 'ip_address' : socket.gethostbyname(fdqn), 'online': False}
        threads.append(Thread(target=is_online,args=(computers.loc[idx]['ip_address'], ping_results, idx)))
        threads[idx].start()
        #computers[idx]['online'] = is_online(computers[idx]['fdqn'])

    print('Pinging hosts', end ='')
    for thread in threads:
        while thread.is_alive():
            print('.', end = '')
            sleep(0.5)
    
    computers['online'] = ping_results
    return computers

def psexec_runner(cmd, host, idx, results, user='', password=''):
    command_string = f'psexec.exe -s \\\\{host} {cmd}'
    try:
        results[idx] = subprocess.run(command_string, capture_output=True, text=False).returncode
    except subprocess.CalledProcessError as e:
        results[idx] = e.output
    

 

class interface:
    def __init__(self):        
        while True:
            command = input('Enter the command to be executed remotely: ')
            dn = input('Enter the AD dn (distinguished name) to select targets from: ')
            computer_df = pd.DataFrame(generate_host_list(dn))
            computer_df = self.__select_targets(computer_df)
            computer_df['result'] = self.__send_command(computer_df, command)['result']
            pprint(f'\n{command} ran against all target with the following results:\n')
            pprint(computer_df)
            if input('Enter "x" to exit, any other key to run again: ').lower() == 'x': break

    def __select_targets(self, computer_df):
        '''Accepts computer_df
        Returns selections from computer_df'''
        while True:
            print(f'\n\n\n\n{computer_df[computer_df["online"] == True].count()[0]}/{computer_df.count()[0]} computers were reachable:\n')
            print(computer_df[computer_df["online"] == True])
            user_input = input('Enter the number index number of the machine to select, "a" for all, or "n" for none: ').lower()
            try:
                computer_df[computer_df["online"] == True].loc[int(user_input)]
                return computer_df[computer_df["online"] == True].loc[int(user_input):int(user_input)]
            except:
                if user_input == 'a':
                    return computer_df[computer_df["online"] == True]
                elif user_input == 'n':
                    break
    
    def __send_command(self, df, cmd):
        '''Sends a command to all machines in a dataframe
        Asks for confirmation first'''
        threads = []
        results = []
        print(f'\n\nThe command "{cmd}" is about to be run on the following machine(s): \n {df}')
        while True:
            confirm = input('Enter "y" to confirm, "n" to exit :').lower()
            if confirm == 'y':                
                for idx, ip in enumerate(list(df['ip_address'])):   
                    results.append('')             
                    threads.append(Thread(target=psexec_runner, args=(cmd, ip, idx, results)))
                    threads[idx].start()
                print('Attempting remote execution on hosts....', end ='')    
                break
            elif confirm == 'n':
                break       
        for thread in threads:
            while thread.is_alive():
                print('.', end = '')
                sleep(0.5)
        df['result'] = results
        return df




if __name__ == "__main__":     


    interface()

    