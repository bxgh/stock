import winrm
s = winrm.Session('192.168.97.66', auth=('wwsa518@outlook.com', 'Hotm@9035065'))

r = s.run_cmd('ipconfig', ['/all'])
