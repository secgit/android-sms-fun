import subprocess
import sqlite3
import nltk
from nltk.collocations import *
from colorama import init, Fore, Back, Style
init(autoreset=True)

allwords = list()
lines = list()
bigrams = list()

pullfb = 'adb pull /data/data/com.facebook.orca com.facebook.orca'
pullsms = 'adb pull /data/data/com.android.providers.telephony/databases/mmssms.db mmssms.db'
pullgosms = 'adb pull /data/data/com.jb.gosms/databases/gommssms.db gommssms.db'
whatsapp_MSG = 'adb pull /data/data/com.whatsapp/databases/msgstore.db msgstore.db'
whatsapp_WA = 'adb pull /data/data/com.whatsapp/databases/wa.db wa.db'

def menu():
	while True:
		options = {1 : checkRoot,
				   2 : getAll,
				   3 : extractWords,
				   4 : getImages,
				   5 : cracklock,
				   6 : exploit,
				   7 : dumpSD,
		}
		print (Fore.CYAN + 
		   'What would you like to do?\n\
	 1) Check for adb & root\n\
	 2) Pull SMS databases (default, WhatsApp, Facebook, GoSMS)\n\
	 3) Extract words & Analyze data\n\
	 4) Pull MMS & Images\n\
	 5) Crack lockscreen pattern\n\
	 6) Attempt to gain root\n\
	 7) Dump sdcard (works w/out root)\n\
	 8) Exit\n\nChoice:'),
		choice = raw_input()
		if choice=='8': break
		options[int(choice)]()
def cracklock():
	print 'crackit'
def dumpSD():
	print 'dumpit'
def exploit():
	print 'popit'
def checkRoot():
	print("[*] Trying 'adb root'...")
	proc = subprocess.Popen(['adb', 'root'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
	if "already running as root" in proc:
		print (Fore.RED + "[*] We're root!")
	else:
		print (Fore.RED + "[*] Not root, try an exploit!")
def getAll():
	print (Fore.RED + '[*] Pulling SMS database')
	subprocess.check_output(pullsms.split())
	print (Fore.RED + '[*] Checking for Facebook messenger')
	subprocess.check_output(pullfb.split())
	print (Fore.RED + '[*] Checking for GoSMS')
	subprocess.check_output(pullgosms.split())
	print (Fore.RED + '[*] Checking for Whatsapp')
	subprocess.check_output(whatsapp_MSG.split())
	subprocess.check_output(whatsapp_WA.split())
	print (Fore.RED + '[*] Checking for Google Voice')

def extractWords():
	conn = sqlite3.connect('mmssms.db')
	c = conn.cursor()
	c.execute('SELECT c1index_text FROM words_content')

	f = open('words.txt','w')
	print (Fore.RED + '[*] Loading lists')
	for record in c.fetchall():
		line = record[0].encode('utf-8').strip()
		words = line.split()
		for eachword in words:
			allwords.append(eachword.lower())
		f.write(record[0].encode('utf-8').strip())
		f.write('\n')
	#f.close()
	allwords.sort()
	analyze()

def getImages():
	print (Fore.RED + '[*] Pulling images')
	pullSMS = 'adb pull /sdcard/DCIM/Camera images'
	s = subprocess.check_output(pullSMS.split())
	print (Fore.RED + '[*] Saved to folder: images')
	#print s

def analyze():
	raw = open("words.txt", "r").read()
	#print raw
	tokens = nltk.word_tokenize(raw)
	text = nltk.Text(tokens)
	fd = nltk.FreqDist(text)
	#print text.concordance("love")
	while True:
		print (Fore.CYAN + '\
		 1) Word search w/ context\n\
		 2) Count occurrences of a word\n\
		 3) Investigate numeric messages w/ context\n\
		 4) Parse street addresses\n\
		 5) List most frequent 20 words\n\
		 6) Back to Main Menu\nChoice:'),
		choice = raw_input()
		if choice=='1':
			word_to_search = raw_input("\nEnter a word: ")
			text.concordance(word_to_search, lines=50)
		if choice=='5':
			most_freq_w = fd.keys()[:20]
			i = 0
			for eachword in most_freq_w:
				print str(i) + ". " + eachword
				i = i + 1
		if choice=='3':
			numbers = sorted([item for item in set(text) if item.isdigit() and (len(item) > 1)])
			#print numbers
			for eachthing in numbers:
				text.concordance(eachthing)
		if choice=='2':
			word_to_count = raw_input("\nEnter a word: ")
			print fd[word_to_count]
		if choice=='6':
			break

print (Fore.CYAN + '\nWelcome!'),
menu()
