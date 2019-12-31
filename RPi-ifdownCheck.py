#!/usr/bin/env python3.7

import sys
import os
from datetime import datetime, timedelta
import configparser
import time

SETTINGS = []
SLEEP_DURATION_MINIMUM = 10
IFACE_STATUS_FILE_PATH = None
IFACE_DOWN_OPERSTATE_STATUS = 'down'

def getSettings():

	global SETTINGS
	settings_filename = './settings.ini'

	config = configparser.ConfigParser()
	config.read(settings_filename)

	# If settings file is missing, print error to CLI and Exit
	if not config.sections():
		print("ERROR: "+ settings_filename + " is missing. Exiting...")
		sys.exit(1)

	# File exists, check sections and options are present. If not, print error to CLI and Exit.
	for section in [ 'Settings' ]:
		if not config.has_section(section):
			print("ERROR: Missing config file section: " + section +". Please check " + settings_filename)
			sys.exit(1)

	if section == 'Settings':
		for option in [ 'ifaceToMonitor', 'SleepDuration' ]:
			if not config.has_option(section, option):
				print("ERROR: Missing Settings option: " + option +". Please check " + settings_filename)
				sys.exit(1)

	# Settings file sections and options valid. Now retrieve/parse values and store in global Settings dict
	try:
		SETTINGS = {
			'IFACE':config.get('Settings', 'ifaceToMonitor'),
			'SLEEP_DURATION':config.getint('Settings', 'SleepDuration')}

	except ValueError as e:
		print("ERROR: Unable to parse values from settings file: \n" + str(e))
		sys.exit(1)

	######## DEBUGGING #########
	# print("DEBUG: Iface Setting set to: "+ SETTINGS['IFACE'])
	# print("DEBUG: Sleep Duration Setting set to: "+ SETTINGS['SLEEP_DURATION'])
	############################

def validateSettings():

	global SETTINGS
	global SLEEP_DURATION_MINIMUM
	global IFACE_STATUS_FILE_PATH

	# Check Iface Status File exists, if not report error and exit
	IFACE_STATUS_FILE_PATH = '/sys/class/net/' + SETTINGS['IFACE'] + '/operstate'
	if not(os.path.exists(IFACE_STATUS_FILE_PATH)):
		print("ERROR: Network Interface " + SETTINGS['IFACE'] + " defined in the Settings file does not exist")
		sys.exit(2)
	# Check Sleep Duration Setting is valid, if not report error and exit
	if SETTINGS['SLEEP_DURATION'] < SLEEP_DURATION_MINIMUM:
		print("ERROR: Sleep Duration Setting is set to " + str(SETTINGS['SLEEP_DURATION']) + ". Minimum Duration is " + str(SLEEP_DURATION_MINIMUM))
		sys.exit(2)

def isIfaceDown():

	global SETTINGS
	global IFACE_STATUS_FILE_PATH
	global IFACE_DOWN_OPERSTATE_STATUS

	with open(IFACE_STATUS_FILE_PATH) as f:
		iface_status = f.read().replace('\n', '')

	print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " : Iface OPERSTATE file for "+ SETTINGS['IFACE'] + " contains " + "'" + iface_status + "'")

	if iface_status == IFACE_DOWN_OPERSTATE_STATUS:
		print (datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " : Iface " + SETTINGS['IFACE'] + " is down.")
		# Interface is down. Return True.
		return True

	# Interface is not down. Return False.
	return False

def shutdownSystem():
	# Final check of Iface status prior to system shutdown
	if isIfaceDown():
		print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " : 2nd Check Completed. Shutting down system now...")
		os.system("shutdown now -h")
		sys.exit(0)

def main():

	global SETTINGS
	global IFACE_STATUS_FILE_PATH
	global IFACE_DOWN_OPERSTATE_STATUS

	if isIfaceDown():
		#Iface is down. Sleep for duration defined in Settings file
		scheduledShutdownDateTime = datetime.now() + timedelta(seconds=SETTINGS['SLEEP_DURATION'])
		print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " : System Shutdown scheduled in " + str(SETTINGS['SLEEP_DURATION']) + " seconds at " + scheduledShutdownDateTime.strftime("%m-%d-%Y %H:%M:%S"))
		print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " : Waiting until " + scheduledShutdownDateTime.strftime("%m-%d-%Y %H:%M:%S") + "...")
		time.sleep(SETTINGS['SLEEP_DURATION'])
		shutdownSystem()

	#Iface is not down. No action required.
	print(datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " : Iface " + SETTINGS['IFACE'] + " is not '" + IFACE_DOWN_OPERSTATE_STATUS +"'. No action required.")

if __name__ == '__main__':

	# First check that script is being run as root user.
	if not os.geteuid() == 0:
		print("ERROR: This Python script must be run as root.")
		sys.exit(1)
	# Script is being run as root. Continue...
	getSettings()
	validateSettings()
	main()
	sys.exit(0)
