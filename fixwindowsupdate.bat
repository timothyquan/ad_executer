net stop wuauserv
net stop DoSvc
net stop cryptSvc
net stop bits
net stop msiserver
Ren C:\Windows\SoftwareDistribution SoftwareDistribution.%DATE:~-4%-%DATE:~4,2%-%DATE:~7,2%.%TIME%.old
Ren C:\Windows\System32\catroot2 Catroot2.%DATE:~-4%-%DATE:~4,2%-%DATE:~7,2%.%TIME%.old
reg delete HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU /v UseWUServer /f
reg add HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\DeliveryOptimization\Config /v DODownloadMode /t REG_DWORD /d 1 /f
reg add HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\DeliveryOptimization\Config /v DownloadMode_BackCompat /t REG_DWORD /d 1 /f
reg add HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\DeliveryOptimization /v DODownloadMode /t REG_DWORD /d 1 /f
net start cryptSvc
net start bits
net start msiserver
net start DoSvc
net start wuauserv
USOClient.exe ScanInstallWait

