### for windows machine ###

import sys
import paramiko as pm
sys.stderr = sys.__stderr__
import os

class AllowAllKeys(pm.MissingHostKeyPolicy):
    def missing_host_key(self, client, hostname, key):
        return

##########################################
HOST = '172.16.106.91'
PORT = 22
USER = 'pi'
PASSWORD = 'raspberry'

#########################################

client = pm.SSHClient()
client.load_system_host_keys()
#client.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
client.set_missing_host_key_policy(AllowAllKeys())
client.connect(HOST, username=USER, password=PASSWORD)

channel = client.invoke_shell()
stdin = channel.makefile('wb')
stdout = channel.makefile('rb')

cmd ='''
pwd
sudo shutdown -h now
exit
'''		# HRAD_CODED : rec_shiv

print "-------SHUTTING DOWN------"
stdin.write(cmd)
print stdout.read()

stdout.close()
stdin.close()
client.close()

print ' ********* OK ******* '

