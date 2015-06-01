import numpy as np
from math import sqrt
import math
import Levenshtein as lv

def create_file_vocab(f_in,f_out):
    eng = matlab.engine.start_matlab()
    tf = 'false'
    tf = eng.noise_canc2(f_in,f_out)
    eng.quit()
    return tf

def create_corpus(f_in):
    with open(f_in) as f:
        c = []
        p = []
        for line in f:
            c.append(line.split())
            p.append(line.split())
    j = 1
    c[0][0] = 1
    p[0][0] = 1
    for i in range(1,len(c)):
        c[i][0] = int(c[i][0])
        if c[i][0] < c[i-1][0]:
            j = j +1
        p[i][0] = j
    tf = False
    i = 0
    while tf is False:
        if p[i][3] is 'V' or p[i][3] is 'D' or p[i][3] is 'O' or p[i][3] is 'L' or p[i][3] is 'A' or p[i][3] is 'R' or p[i][3] is '!' or p[i][3] is 'P' or p[i][3] is '&' or p[i][3] is 'T' or p[i][3] is 'X' or p[i][3] is 'Y' or p[i][3] is '~' or p[i][3] is 'U' or p[i][3] is 'E' or p[i][3] is ',' or p[i][3] is 'G' or p[i][3] is '$' or p[i][3] is '@':
            del p[i]
        else:
            i = i +1
        if i >= len(p):
            tf = True
    corpus = []
    corpus.append(p[0][1])
    j = 0
    for i in range(1,len(p)):
        if p[i][0] is p[i-1][0]:
            corpus[j] = corpus[j] + ' ' + p[i][1]
        else:
            j = j +1
            corpus.append(p[i][1])
    return corpus

def cosine_sim(v1,v2):
    return float(np.dot(v1,v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

def vectorize(sentence, vocab):
    s = [0] * len(vocab)
    d = sentence.split()
    for i in d:
        m = 1.0
        for j in vocab:
            a = float(lv.distance(i,j))
            b = float(len(i))
            if a/b < m:
                m = a/b
                ind = vocab.index(j)
        if m < 0.3:
            s[ind] = 1
    return s

def create_vect_text_corpus(mycorpus,vocab):
    vectorized_corpus = []
    for i in mycorpus:
        vectorized_corpus.append((i, vectorize(i, vocab)))
    return vectorized_corpus

def create_vect_text_corpus2(mycorpus,vocab):
    def vectorize2(sentence, vocab):
        return [sentence.split().count(i) for i in vocab]
    vectorized_corpus = []
    for i in mycorpus:
        vectorized_corpus.append((i, vectorize2(i, vocab)))
    return vectorized_corpus

def create_vocab_from_file(f_name):
    with open(f_name) as f:
        mydict = list()
        for line in f:
            #s = line.split()
            if line.strip().lower() not in mydict:
            #if s not in mydict:
            #mydict [key] = s
            #mydict [key] = line.strip().lower()
                mydict.append(line.strip().lower())
    mydict.pop(0)
    vocab = sorted(mydict)
    return vocab
    
    
def test_sim(vcorpus):
    sim = []
    for i in range(0,len(vcorpus)):
        for j in range(i+1,len(vcorpus)):
            sim.append([i,j,cosine_sim(np.asarray(vcorpus[i][1]),np.asarray(vcorpus[j][1]))])
    return sim


def event_detection(f_conn,voc,f_corp,th):
	corpus = create_corpus(f_corp)
	print 'corpus successfully created'
	f=open(f_conn,'w')
	f.write('0')
	f.close()
	print 'comparing tweets...'
	#voc = create_vocab_from_file(f_voc)
	#print 'vocab successfully created from file'
	vcorpus = create_vect_text_corpus(corpus,voc)
	print 'corpus successfully vectorized'
	event = []
	e_list = []
	lsim = []
	tw_good = 0
	tw_rep = 0
	ecount = np.zeros(len(vcorpus))
	event.append(([vcorpus[0][0]],0))
	e_list.append(0)
	ecount[0] = ecount[0] +1
	for i in range(1,len(vcorpus)):
		ind = 0;
		control = False
		s = cosine_sim(np.asarray(vcorpus[i][1]),np.asarray(vcorpus[0][1]))
		if math.isnan(s):
			s_max = 0.0
		else:
			s_max = s
			control = True
		for j in range(0,i-1):
			s = cosine_sim(np.asarray(vcorpus[i][1]),np.asarray(vcorpus[j][1]))
			if s >= s_max and not math.isnan(s):
				if s > s_max:
					s_max = s
					ind = j
				control = True
		lsim.append([s_max,ind])
		if s_max < 0.9:
			if control is True:
				tw_good = tw_good +1
				if s_max < th:
					event.append(([vcorpus[i][0]],i))
					e_list.append(i)
					ecount[i] = ecount[i] +1
				else:
					if ind in e_list:
						ecount[ind] = ecount[ind] +1
						event[[y[1] for y in event].index(ind)][0].append(vcorpus[i][0])
		else:
			tw_rep = tw_rep +1
	event_good=[]
	for i in event:
		if len(i[0]) > 1:
			event_good.append(i[0])
	print '\n'
	print 'event'
	print event
	print '\n'
	print 'event filtered'
	print event_good
	print '\n'
	print 'events associated to each tweet'
	print ecount
	print '\n'
	print 'max similarity for each tweet'
	print lsim
	print '\n'
	print 'tweets containing words contained in our dictionary'
	print tw_good
	print '\n'
	print 'tweets repeated eliminated-spam'
	print tw_rep
	return (event,event_good,ecount,lsim,tw_good,tw_rep)
        


#(ev,c,lsim,tw_good,tw_rep) = event_detection('dic.txt','tweets3g.txt',0.3)

#print ev
#print c
#print lsim
#print tw_good
#print tw_rep

#a = []
#for i in range(len(vcorpus)):
#    tot1 = 0
#    for j in range(len(vcorpus[i][1])):
#        tot1 = tot1 + vcorpus[i][1][j]
#    a.append(tot1)

#tf = create_file_vocab('voctot.txt','dic.txt')

#corpus = create_corpus('tweets3g.txt')
#th = 0.3
#voc = create_vocab_from_file('dic.txt')
#vcorpus = create_vect_text_corpus2(corpus,voc)
#event = []
#e_list = []
#lsim = []
#tw_good = 0
#tw_rep = 0
#ecount = np.zeros(len(vcorpus))
#event.append(([vcorpus[0][0]],0))
#e_list.append(0)
#ecount[0] = ecount[0] +1
#for i in range(1,len(vcorpus)):
#    ind = 0;
#    control = False
#    s = cosine_sim(np.asarray(vcorpus[i][1]),np.asarray(vcorpus[0][1]))
#    if math.isnan(s):
#        s_max = 0.0
#    else:
#        s_max = s
#        control = True
#    for j in range(0,i-1):
#        s = cosine_sim(np.asarray(vcorpus[i][1]),np.asarray(vcorpus[j][1]))
#        if s >= s_max and not math.isnan(s):
#            if s > s_max:
#                s_max = s
#                ind = j
#            control = True
#    lsim.append([s_max,ind])
#    if s_max < 0.9:
#        if control is True:
#            tw_good = tw_good +1
#            if s_max < th:
#                event.append(([vcorpus[i][0]],i))
#                e_list.append(i)
#                ecount[i] = ecount[i] +1
#            else:
#                if ind in e_list:
#                    ecount[ind] = ecount[ind] +1
#                    event[[y[1] for y in event].index(ind)][0].append(vcorpus[i][0])
#    else:
#        tw_rep = tw_rep +1








