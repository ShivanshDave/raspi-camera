### for windows machine ###

import sys
import paramiko as pm
sys.stderr = sys.__stderr__
import os

class AllowAllKeys(pm.MissingHostKeyPolicy):
    def missing_host_key(self, client, hostname, key):
        return

##########################################
HOST = '172.16.106.66'
PORT = 22
USER = 'pi'
PASSWORD = 'raspberry'

pi_record_folder = 'recordings' 	#inside "rec_shiv" folder

filename = 'ncbs'
Time_Segment = '3*1000'				# in milliseconds
Num_of_Segments = '3'

WW = '640'
HH = '480'
FPS = '60'

#########################################

client = pm.SSHClient()
client.load_system_host_keys()
#client.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
client.set_missing_host_key_policy(AllowAllKeys())
client.connect(HOST, username=USER, password=PASSWORD)

channel = client.invoke_shell()
stdin = channel.makefile('wb')
stdout = channel.makefile('rb')

import time
Dt_Set = 'sudo date -s "' +time.strftime("%c")+'"'

REC='for var in {1..'+Num_of_Segments+'}; do raspivid --width '+WW+' --height '+HH+' --framerate '+FPS+' --timeout $(('+Time_Segment+')) --output '+filename+'_dt-$(date +"%d-%m_time-%H-%M-%S").h264; done'

cmd ='''
pwd
'''+ Dt_Set +'''
mkdir rec_shiv
cd rec_shiv
mkdir '''+ pi_record_folder +'''
cd '''+ pi_record_folder +'''
'''+ REC +'''
ls -l
exit
'''		# HRAD_CODED : rec_shiv

print "-------RECORDING in PROGRESS------"
stdin.write(cmd)
print stdout.read()

stdout.close()
stdin.close()
client.close()
print "-------RECORDING over SSH is DONE------"
#http://stackoverflow.com/questions/6203653/how-do-you-execute-multiple-commands-in-a-single-session-in-paramiko-python

##----------------------------------------------------------------##

print "-------Downloading all the files-------"

windows_folder = os.getcwd() + '\REC-' + time.strftime("%d-%m-%Y")			# HRAD_CODED : CWD

note= '***--- Storing at : ' + windows_folder + ' ---***'
print note

if not os.path.exists(windows_folder):
	os.makedirs(windows_folder)
cmd = 'pscp.exe -pw ' + PASSWORD + ' ' + USER + '@' + HOST + ':/home/pi/rec_shiv/'+ pi_record_folder +'/*.* "' + windows_folder +'"'  # HRAD_CODED : rec_shiv
print cmd
os.system(cmd)
print "-------Downloading done-------"
#http://stackoverflow.com/questions/10235778/scp-from-linux-to-windows

##----------------------------------------------------------------##

print "-------Converting all the files-------"

for filename in os.listdir(windows_folder):
	if filename[-3:] == '264': 
		input_file = os.path.join(windows_folder, filename)
		output_file = os.path.join(windows_folder, filename[:-4]+'avi')
		cmd = 'ffmpeg -y -r 10 -i ' + input_file + ' -vcodec copy ' + output_file
		os.system(cmd);
		cmd = 'del '+input_file
		os.system(cmd);

print ' ********* OK ******* '

