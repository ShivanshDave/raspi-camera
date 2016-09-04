### for windows machine ###

import sys
import paramiko as pm
sys.stderr = sys.__stderr__
import os

##########################################
HOST = '172.16.106.66'
PORT = 22
USER = 'pi'
PASSWORD = 'raspberry'

pi_record_folder = 'recordings'

#########################################

import time

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

