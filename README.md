android-sms-fun
====================

 **Dump common Android SMS databases and use the Python Natural Language Toolkit (NLTK) to discover interesting information.**  
  
Supported apps:  
-Facebook Messenger  
-GoSMS  
-Android's default 'mmssms.db'  
-WhatsApp (only dumps .db)


Requirements
------------
Python 2.7  
NLTK  
sqlite3  
USB debugging & root  


Usage
-----
Obtain a phone with USB debugging enabled  
Plug phone into PC  

C:\>python android-sms-fun.py  
  
Welcome! What would you like to do?  
         1) Check for adb & root  
         2) Pull SMS databases (default, WhatsApp, Facebook, GoSMS)  
         3) Extract words & Analyze data  
         4) Pull MMS & Images  
         5) Dump sdcard  
         6) Get sensitive data (accounts.db)    
         7) Exit  
Choice:  
  
Option 3 expands to...  
1) Word search w/ context  
2) Count occurrences of a word  
3) Investigate numeric messages w/ context  
4) Parse street addresses  
5) List most frequent 20 words  
6) Back to Main Menu  
