#Author: github.com/secgit
#Date: 12-18-2013
#Purpose: 
#  Dump common Android SMS databases and use the Python Natural
#  Language Toolkit (NLTK) to discover interesting information.

import subprocess
import sqlite3
import nltk
import os.path
from nltk.collocations import *

allwords = list()

pullfb = 'adb pull /data/data/com.facebook.orca/databases/threads_db2 .'
pullsms = 'adb pull /data/data/com.android.providers.telephony/databases/mmssms.db .'
pullgosms = 'adb pull /data/data/com.jb.gosms/databases/gommssms.db .'
whatsapp_MSG = 'adb pull /data/data/com.whatsapp/databases/msgstore.db .'
whatsapp_WA = 'adb pull /data/data/com.whatsapp/databases/wa.db .'
sdcard = 'adb pull /mnt/sdcard .'
sensitive = 'adb pull /data/system/accounts.db .'

def menu():
	while True:
		options = {1 : checkRoot,
				   2 : getAll,
				   3 : extractWords,
				   4 : getImages,
				   5 : dumpSD,
				   6 : getSensitive,
		}
		print "What would you like to do?\n\
	 1) Check for adb & root\n\
	 2) Pull SMS databases (default, WhatsApp, Facebook, GoSMS)\n\
	 3) Extract words & Analyze data\n\
	 4) Pull MMS & Images\n\
	 5) Dump sdcard\n\
	 6) Get sensitive data (accounts.db)\n\
	 7) Exit\n\nChoice:",
		choice = raw_input()
		if choice.isdigit() == True:
			if choice=='7': break
			else:
				options[int(choice)]()
		else:
			continue
def checkRoot():
	print "[*] Trying 'adb root'..."
	proc = subprocess.Popen(['adb', 'root'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
	if "already running as root" in proc:
		print "[*] We're root!"
	else:
		print "[*] Not root, try an exploit!"
def getAll():
	print "[*] Pulling SMS database"
	subprocess.check_output(pullsms.split())
	print "[*] Checking for Facebook messenger"
	subprocess.check_output(pullfb.split())
	print "[*] Checking for GoSMS"
	subprocess.check_output(pullgosms.split())
	print "[*] Checking for Whatsapp"
	subprocess.Popen(whatsapp_MSG.split()).communicate()[0]
	subprocess.Popen(whatsapp_WA.split()).communicate()[0]

def extractWords():
	if os.path.exists('mmssms.db') == False:
		print "\n[*] Use option 2 to dump the databases first!"
		return
	else:
		print "[*] Extracting words..."
		
		conn = sqlite3.connect('mmssms.db')
		c = conn.cursor()
		c.execute('SELECT c1index_text FROM words_content')
		
		f = open('words.txt','w')
		for record in c.fetchall():
			#print record[0]
			line = record[0].encode('utf-8').strip()
			words = line.split()
			for eachword in words:
				allwords.append(eachword.lower())
			f.write(record[0].encode('utf-8').strip())
			f.write('\n')
		f.close()
	if os.path.exists('threads_db2'):
		conn = sqlite3.connect('threads_db2')
		c = conn.cursor()
		c.execute('SELECT text FROM messages')
		
		f = open('words.txt','a')
		for record in c.fetchall():
			line = str(record[0])
			words = line.split()
			for eachword in words:
				allwords.append(eachword.lower())
			f.write(str(record[0]))
			f.write('\n')
		f.close()
	if os.path.exists('gommssms.db'):
		conn = sqlite3.connect('gommssms.db')
		c = conn.cursor()
		c.execute('SELECT c1index_text FROM words_content')
		
		f = open('words.txt','a')
		for record in c.fetchall():
			line = record[0].encode('utf-8').strip()
			words = line.split()
			for eachword in words:
				allwords.append(eachword.lower())
			f.write(record[0].encode('utf-8').strip())
			f.write('\n')
		f.close()
	analyze()

def getImages():
	print "[*] Pulling images"
	pullSMS = 'adb pull /sdcard/DCIM/Camera images'
	s = subprocess.check_output(pullSMS.split())
	print "[*] Saved to folder: images"
	#print s

def analyze():
	allwords.sort()
	raw = open("words.txt", "r").read()
	tokens = nltk.word_tokenize(raw)
	text = nltk.Text(tokens)
	fd = nltk.FreqDist(text)
	while True:
		print "\
		 1) Word search w/ context\n\
		 2) Count occurrences of a word\n\
		 3) Investigate numeric messages w/ context\n\
		 4) Parse street addresses\n\
		 5) List most frequent 20 words\n\
		 6) Back to Main Menu\nChoice:",
		choice = raw_input()
		if choice=='1':
			word_to_search = raw_input("\nEnter a word: ")
			text.concordance(word_to_search, lines=50)
		if choice=='2':
			word_to_count = raw_input("\nEnter a word: ")
			print fd[word_to_count]
		if choice=='3':
			numbers = sorted([item for item in set(text) if item.isdigit() and (len(item) > 1)])
			#print numbers
			for eachthing in numbers:
				text.concordance(eachthing)
		if choice=='4':
			text.concordance('av')
			text.concordance('ave')
			text.concordance('st')
			text.concordance('blvd')
			text.concordance('rd')
		if choice=='5':
			most_freq_w = fd.keys()[:20]
			i = 0
			for eachword in most_freq_w:
				print str(i) + ". " + eachword
				i = i + 1
		if choice=='6':
			break

def dumpSD():
	print "[*] Dumping SD card..."
	subprocess.check_output(sdcard.split())
def getSensitive():
	print "[*] Pulling accounts.db..."
	subprocess.check_output(sensitive.split())
	
	connfb = sqlite3.connect('accounts.db')
	c = connfb.cursor()
	c.execute('SELECT name FROM accounts')
	print "[*] Printing accounts..."
	for record in c.fetchall():
		print str(record[0])
	c.execute('SELECT password FROM accounts')
	print "[*] Printing password hashes"
	for record in c.fetchall():
		print str(record[0])

print "\nWelcome!",
menu()
