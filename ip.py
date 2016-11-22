#!/usr/bin/python3

import smtplib
import subprocess
import os
import time

LAST_IP = None


def write_updated_ip(ip):
	file = open("ip", "w")
	file.write(ip)
	file.close()

	os.system("git pull")
	os.system("git add ip")
	os.system("git commit -m 'script updating ip'")
	os.system("git push")

def write_no_update_log():
	file = open("log", "w")
	file.write("\n" + time.strftime("%a, %d %b %Y %H:%M:%S"))
	file.close()

	os.system("git pull")
	os.system("git add log")
	os.system("git commit -m 'script updating log'")
	os.system("git push")

def check_ip():
	global LAST_IP

	command = ["curl", "icanhazip.com"]
	external_ip = subprocess.Popen(command, stdout=subprocess.PIPE ).communicate()[0]
	external_ip = external_ip.decode("ASCII")

	if LAST_IP != external_ip:
		print("IP updated from", LAST_IP, "to", external_ip)
		write_updated_ip(external_ip)
		LAST_IP = external_ip
	else:
		print("checked IP, no change")
		write_no_update_log()

def load_past_ip():
	global LAST_IP
	file = open("ip", "r")
	past_ip = file.read(64)
	if past_ip:
		print("Found past IP", past_ip)
		LAST_IP = past_ip


load_past_ip()
check_ip()
while(True):
	time.sleep(12 * 60 * 60) # 12 hours in seconds
	check_ip()
