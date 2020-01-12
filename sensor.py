#!/usr/bin/python

import os
import glob
import time
from datetime import datetime

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

tempsC = []
tempsF = []
resolution = 299 # Subtract 1 from desired interval to account for time drift (5 minutes)
runsPerAvg = 6 # 30 minutes
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines

def read_temp():
	lines = read_temp_raw()
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw()
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string) / 1000.0
		# temp_f = round((temp_c * 9.0 / 5.0 + 32.0), 3)
	return temp_c

print("This saves 2 files: tempLog.csv, and tempLogVerbose.csv.")
print("tempLog.txt contains averages of readings taken every 5 minutes (or time specified), with the timestamp being that of the last reading.")
print("tempLogVerbose contains every single temperature reading taken, with timestamps indicating time taken.")

while True:
	i=0
	while i < runsPerAvg:
		tempC = read_temp()
		tempF = round((tempC * 9/5 + 32), 3)
		tempsC.append(tempC)
		tempsF.append(tempF)
		now = datetime.now()
		timeStr = now.strftime("%m/%d/%Y,%H:%M:%S")
		out = "{0},{1},{2}".format(timeStr, tempC, tempF)
		print(out)
		with open("tempLogVerbose.csv", "a") as verbose:
			if os.stat("tempLogVerbose.csv").st_size == 0:
				verbose.write("date,time,c,f\n")
			out = "{0}\n".format(out)
			verbose.write(out)
		i += 1
		time.sleep(resolution) # seems to execute 1 second slow on my Pi, might just be a slow system
	avgC = round((sum(tempsC)/len(tempsC)), 3)
	avgF = round((sum(tempsF)/len(tempsF)), 3)
	now = datetime.now()
	timeStr = now.strftime("%m/%d/%Y,%H:%M:%S")
	avgOut = ("{0},{1},{2}").format(timeStr, avgC, avgF)
	print("Saving Average...")
	with open("tempLog.csv", "a") as file:
		if os.stat("tempLog.csv").st_size == 0:
			file.write("date,time,c,f\n")
		avgOut = ("{0}\n").format(avgOut)
		file.write(avgOut)
		tempsC = []
		tempsF = []
