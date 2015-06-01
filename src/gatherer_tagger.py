consumer_key='6gnDRuDirRPO9tnOcEm2NWS56'
consumer_secret='Blf7cPIVJRff2HnkW8MPkG2TmAgnGmxULGSpxuJU1zFi7gucWN'
access_token='3094079105-kekHTJUfFVE1q99VlHhG9nQmBEHx9Ov3lMJqrKq'
access_token_secret='tswdm5jUZFaqkwKQi2kVATkj21ilq9gKbnfuYZAhFvGUM'
tweets_number=500


import numpy as np
from math import sqrt
import math
import Levenshtein as lv
import urllib3.contrib.pyopenssl
urllib3.contrib.pyopenssl.inject_into_urllib3()

import os
import sys
import tweepy
import codecs
import webbrowser
import json
import time
from multiprocessing import Process

#QUESTO FILE:
"""
	-SCARICA I TWEET FORMATTATI IN .JSON O .TXT (UN TWEET PER RIGA IN QUESTO CASO)
	-FILTRA I TWEET IN LINGUA INGLESE (APPROSSIMATIVMENTE) (ED ELIMINA I '\n')
	-(ora inutile) PULISCE IL FILE DALLE RIGHE VUOTE
"""

def gatherer(consumer_key,consumer_secret,access_token,access_token_secret,tw_number):
	# Consumer keys and access tokens, used for OAuth
	#consumer_key = '6gnDRuDirRPO9tnOcEm2NWS56'
	#consumer_secret = 'Blf7cPIVJRff2HnkW8MPkG2TmAgnGmxULGSpxuJU1zFi7gucWN'
	#access_token = '3094079105-kekHTJUfFVE1q99VlHhG9nQmBEHx9Ov3lMJqrKq'
	#access_token_secret = 'tswdm5jUZFaqkwKQi2kVATkj21ilq9gKbnfuYZAhFvGUM'
	# OAuth process, using the keys and tokens
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	# Creation of the actual interface, using authentication
	api = tweepy.API(auth)
	
	# COUT IS USED TO GIVE AN APPROXIMATION OF HOW MANY TWEETS I'M PULLING AT A GIVEN TIME
	count = []
	f = codecs.open("random.txt","w","utf-8")
	#ff = codecs.open("twiits.txt","w","utf-8")
	
	# DOVREBBE RIMUOVERE CARATTERI NON ASCII
	def remove_non_ascii(text):
		return''.join(i for i in text if ord(i)<128)
	
	class StreamListener(tweepy.StreamListener):
			tweetCounter=0	#static variable
			it=0 #static variable
			
			def on_status(self, status):
				
				#StreamListener.tweetCounter = StreamListener.tweetCounter +1 # SPOSTATO NEL CONDIZIONALE lang="en"
				
				os.system('clear')
				print 'Running...'
				print StreamListener.tweetCounter,' out of ',StreamListener.it
				StreamListener.it=StreamListener.it+1
				info = status.text, status.created_at, status.id
				
				# VARI DECODE UTILI E NON
				#f.write(str(info));
				#f.write(str(status.text.decode('utf-8')))
				
				#QUESTO BOH
				#with open("text.txt", "w") as outfile:
					#json.dump({'text':status.text, 'date':str(status.created_at), 'id':status.id}, outfile, indent=4)
				
				# STAMPA JSON JUSTO
				#json.dump({'text':status.text, 'date':str(status.created_at), 'id':status.id},f,indent=4)
				
				#STAMPA SOLO TESTO, SE INGLESE
				if (status.lang=="en") :
					StreamListener.tweetCounter = StreamListener.tweetCounter +1
					
					# REPLACE '\n' WITH SPACES
					while "\n" in status.text:
						status.text=status.text.replace('\n', ' ')
					
									
					#file prova
					#ff.write(status.text)
					#ff.write("\nEND OF TWEET\n\n")
					#file utilizzato
					f.write(status.text)
					f.write("\n")
				
				for i in info:
					count.append(1)
				
				if StreamListener.tweetCounter < tw_number:
					#f.write("\n")
					return True
				else:
					print 'maxnum = '+str(StreamListener.tweetCounter)
					return False
	
			def on_error(self, status_code):
				print >> sys.stderr, "Encountered error with status code: ", status_code
	
			def on_timeout(self):
				print >> sys.stderr, "Timeout..."
				return True
	
	sapi = tweepy.streaming.Stream(auth, StreamListener(),timeout=300)
	sapi.sample()
	#sapi.filter(track=["fifa","qatar","arrested"])

	f.close()
	os.system('./run2.sh random.txt')
	return

stop=False
while stop is False:
	k=0
	while k is 0:
		print 'tagger is waiting'
		f1=open('fcom.txt','r')
		for line in f1:
			if '0' in line:
				k = 1
				print 'tagger starting'
		f1.close()
		time.sleep(2)
	gatherer(consumer_key,consumer_secret,access_token,access_token_secret,tweets_number)
	ft = codecs.open("random_good.txt","w","utf-8")
	with open("random.txt.predict") as f:
		for line in f:
			if not line.isspace():
				ft.write(line.decode('utf-8'))
	ft.close()
	fc=open('fcom.txt','w')
	fc.write('1')
	fc.close()

