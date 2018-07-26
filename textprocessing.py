# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 07:39:23 2018

@author: 15618
"""
from glob import glob
import pandas as pd
import re
import numpy as np
from nltk.corpus import stopwords
import nltk
from datetime import datetime
import gc
nltk.download("stopwords")
md=pd.read_csv('Middle-NDMC-Dev.csv')
md1=pd.read_csv('Middle-NDMC-Train.csv')
md2=pd.read_csv('Middle-NDMC-Test.csv')
md3=pd.read_csv('Elementary-NDMC-Dev.csv')
md4=pd.read_csv('Elementary-NDMC-Test.csv')
md5=pd.read_csv('Elementary-NDMC-Train.csv')
mdall=pd.concat((md,md1,md2,md3,md4,md5))
del md,md1,md2,md3,md4,md5
lemma=nltk.stem.WordNetLemmatizer()
def tokenize(review, remove_stopwords = True ):
    # Function to convert a document to a sequence of words,
    # optionally removing stop words.  Returns a list of words.
    # 1. Remove non-letters
    review_text = re.sub("[^a-zA-Z0-9]"," ", review)
    # 2. Convert words to lower case and split them
    words = review_text.lower().split()
    # 3. Optionally remove stop words (true by default)
    if remove_stopwords:
        stops = set(stopwords.words("english"))
        words = [lemma.lemmatize(w) for w in words if not w in stops]
    # 5. Return a list of words
    return words
def preprocessing(md):
    quest=md['question']
    split=[re.sub('\([ABCDE12345]\)','999999999',x) for x in quest]
    split=[x.split('999999999') for x in split]
    lenth=np.array([len(x) for x in split])

    split=[split[y] for y in np.argwhere(lenth == 5).reshape((len(np.argwhere(lenth == 5)),))]
    quest=[' '.join(tokenize(x[0])) for x in split]
    ansA=[' '.join(tokenize(x[1])) for x in split]
    ansB=[' '.join(tokenize(x[2])) for x in split]
    ansC=[' '.join(tokenize(x[3])) for x in split]
    ansD=[' '.join(tokenize(x[4])) for x in split]
    ans=md['AnswerKey'].iloc[np.argwhere(lenth == 5).reshape((len(np.argwhere(lenth == 5)),))]
    ans[ans==1]='A'
    ans[ans==2]='B'
    ans[ans==3]='C'
    ans[ans==4]='D'
    return pd.DataFrame({'question':quest,'A':ansA,'B':ansB,'C':ansC,'D':ansD,'ans':ans})
def textbook_smasher(path,min_words=200,deli='\n\n'):
    t1=datetime.now()
    f=open(path,encoding='utf-8')
    tx=f.read()
    tx=re.sub("(?isu)(http\://[a-zA-Z0-9\.\?/&\=\:]+)",' ',tx)
    tx=re.sub("[^A-Za-z0-9%s]"%deli,' ',tx).lower()
    txs=tx.split(deli)
    txss=[]
    for i in range(len(txs)):
        corpa=re.sub('\n',' ',' '.join(tokenize(txs[i])))
        if len(corpa)>min_words:
            txss.append(corpa)
    t2=datetime.now()
    print(t2-t1)
    gc.collect()
    return list(set(txss))


for t in glob('txt/*.txt'):
    studystack=studystack+textbook_smasher(t,deli='\n\n',min_words=40)
bions=textbook_smasher('ck.txt',deli='\n\n',min_words=15)  
studystack=textbook_smasher('studystack7.txt',deli='\n\n',min_words=15)

mdp=preprocessing(mdall)
mdp.to_csv('qna.csv',index=False)