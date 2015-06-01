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

from event_detection import event_detection
from event_detection import create_vocab_from_file

print 'creating dictionary'
voc = create_vocab_from_file('dic2.txt')
print 'vocab successfully created from file'
stop=False
while stop is False:
	k=0
	while k is 0:
		print 'detector is waiting'
		f1=open('fcom.txt','r')
		for line in f1:
			if '1' in line:
				k = 1
				print 'det starting'
		f1.close()
		time.sleep(2)
	(ev,evg,c,lsim,tw_good,tw_rep) = event_detection('fcom.txt',voc,'random_good.txt',0.5)
	f2=open('result.txt','a')
	for x in ev:
		f2.write('events')
		f2.write(x[0][0])
	f2.write('\n')
	for y in evg:
		f2.write('filtered events')
		f2.write(y[0][0])
	f2.close()
	
