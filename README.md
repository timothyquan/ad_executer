# ad_executer
 Script to search in an AD OU for computer names, then executed a command against one or all of them. The execution is performed by 'psexec' in a subprocess call. 

 This script assumes you are on a domain on an account with access to a domain controller and execusion on the remote machines

 Accepts the 'distinguished name' of an OU containing domain computers. https://www.ibm.com/support/knowledgecenter/ssw_ibm_i_71/rzahy/rzahyunderdn.htm

 Accepts a command to be executed on the remote machines.

 There is a text interface for machine selection, results, etc.

 The basic flow is as follows:
 * User enters ou dn when prompted
 * User enters command to be executed on remote machines
 * Script searches the OU for DNs, assumes they are computers
    * The DNs are parsed into fully qualified domain names 
 * Resolve the IP address
 * Execute threaded processes to ping each IP address against all machines simultaneously; parse the results to 'online' status (bool)
 * Create a pandas dataframe with fdqns, IP addresses, online status
 * Prompt the user to select target(s) from one or all of the online machines
 * Execute the command against all selected machines, add results and exit code column to dataframe and display to user

# TODO: 

 * Complete gui
 * Fix encapsulation, put gui and methods in classes