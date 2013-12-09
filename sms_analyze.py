import subprocess
import sqlite3
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
				   3 : getSMSDB,
				   4 : getAppDBS,
				   5 : getImages,
				   6 : analyze,
		}
		print (Fore.CYAN + 
		   'What would you like to do?\n\
	 1) Check if root\n\
	 2) Pull everything (SMS + 3rd party apps)\n\
	 3) Pull SMS\n\
	 4) Pull 3rd party app messages\n\
	 5) Pull MMS\n\
	 6) Analyze data\n\
	 7) Exit\n\nChoice:'),
		choice = raw_input()
		if choice=='7': break
		options[int(choice)]()

def checkRoot():
	print(Fore.RED + '[*] Checking if root...')
	test = subprocess.check_output(['adb', 'root'])
	print test

def getAll():
	print (Fore.RED + '[*] Checking for Facebook messenger')
	subprocess.check_output(pullfb.split())
	print (Fore.RED + '[*] Checking for GoSMS')
	subprocess.check_output(pullgosms.split())
	print (Fore.RED + '[*] Checking for Whatsapp')
	subprocess.check_output(whatsapp_MSG.split())
	subprocess.check_output(whatsapp_WA.split())
	print (Fore.RED + '[*] Checking for Google Voice')
	#getSMSDB()

def getSMSDB():
	print (Fore.RED + '[*] Pulling SMS database')
	s = subprocess.check_output(pullsms.split())
	print s
	print (Fore.RED + '[*] Extracting sqlite tables')
	conn = sqlite3.connect('mmssms.db')
	c = conn.cursor()
	c.execute('SELECT c1index_text FROM words_content')

	#f = open('words.txt','w')
	print (Fore.RED + '[*] Loading lists')
	for record in c.fetchall():
		line = record[0].encode('utf-8').strip()
		words = line.split()
		for eachword in words:
			allwords.append(eachword.lower())
		#f.write(record[0].encode('utf-8').strip())
		#f.write('\n')
	#f.close()
	allwords.sort()

def getAppDBS():
	print ''
def getImages():
	print (Fore.RED + '[*] Pulling images')
	pullSMS = 'adb pull /sdcard/DCIM/Camera images'
	s = subprocess.check_output(pullSMS.split())
	print (Fore.RED + '[*] Saved to folder: images')
	#print s
def analyze():
	print (Fore.CYAN + '\
	 1) Profile user into category\n\
	 2) Most frequently messaged contact\n\
	 3) Most common words/phrases\n\
	 4) Parse addresses + numbers\n\
	 5) Cancel\nChoice:'),
	choice = raw_input()
	#if choice=='5': break

print (Fore.CYAN + '\nWelcome!'),
menu()
#analyze()
