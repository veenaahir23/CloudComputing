from flask import Flask, request, render_template
import requests
import pymysql
import nltk
import nltk
from collections import Counter
from nltk.corpus import stopwords
import collections
import re
import sys
import time
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
import codecs
import os
import nltk
import operator

nltk.download('punkt')



database_instance_endpoint="database-1.cmkbf13rlcv3.us-west-2.rds.amazonaws.com"
port=3306
dbname="veenadatabase"
user="*****"
password="******"

conn = pymysql.connect(database_instance_endpoint,
                      user = user,
                      port = port,
                      passwd = password,
                      database = dbname)
cursor = conn.cursor()

application = Flask(__name__)


@application.route('/')
def home():
    message = "Quiz 6"

    return render_template('home.html')
 
@application.route('/query6', methods=["POST", "GET"])
def mainscreen():
    file = open("Grimm.txt","r")
    text = file.read()
    #res = text.split(' ', 1)[1]
    fnouns = ' '.join(re.findall(r'\b[A-Z][a-z]+|\b[A-Z]\b', text))
    print(fnouns)
    flist = fnouns.split()
    display = []
    num = int(request.form['range1'])

    counter = Counter(flist)
    most_frequent = counter.most_common(num)
    print(most_frequent)

    

    display.append(most_frequent)

    return render_template('query6.html', display = display)

@application.route('/query7', methods=["POST", "GET"])
def query7():
    file = open("Grimm.txt","r")
    text = file.read()
    nouns = {}
    rows = []
    sentences = text.split(".")
    print(sentences)
    for sentence in sentences:
        sentence = sentence.replace('\n','')
        words = sentence.split(" ")
        for word in words[1:]:
            try:
                word = ''.join(e for e in word if e.isalnum())
                if word[0].isupper():
                    if word not in nouns.keys():
                        nouns[word] = 0
                        nouns[word] += 1
            except:
                pass
  
    display = sorted(nouns.items(), key=operator.itemgetter(1), reverse= True)
    print(display)
    return render_template('query7.html', display = display)

@application.route('/question7', methods=["POST", "GET"])
def question7():
    file = open("Grimm.txt","r")
    text = file.read()
    
    text1 = re.findall(r"([^.]*?Brot[^.]*\.)",text)
    text2 = re.findall(r"([^.]*?Auge[^.]*\.)",text)
    text3 = re.findall(r"([^.]*?Augen[^.]*\.)",text)
    text4 = re.findall(r"([^.]*?Baum[^.]*\.)",text)

    print(text1)
    print(text2)

    print(text3)

    print(text4)



    return render_template('question7.html', text1 = text1,text2 = text2,text3 = text3,text4 = text4)


@application.route("/query9", methods=["POST", "GET"])
def query9():
    file = open("Grimm.txt","r")
    x = file.read()
    text0 = x.split()
    #text1 = ' '.join(re.findall(r'\b[A-Z][a-z]+|\b[A-Z]\b', x))
    #text = text1.split()
    print(text0)

    display = []
    index_pos_list = []
    index_pos_list1  = []

    word1 = request.form['word1']
    word2 = request.form['word2']
    n = int(request.form['range'])

   
    for i in range(len(text0)):
        if text0[i] == word1:
            index_pos_list.append(i)
    print(index_pos_list)
    for i in range(len(text0)):
        if text0[i] == word2:
            index_pos_list1.append(i)
    print(index_pos_list1)
    
    for r in range(0,len(index_pos_list)):
        if(r == (n - 1)):
            val =index_pos_list[r]

    for i in index_pos_list:
        if(i == val):
            index1 = i
        #print(text[i:i+10])
        for j in index_pos_list1:
            if(j > val):
                index2 = j
                break
    display = text0[index1:index2+1]
    count = 0
    for items in display:
        count = count + 1



    return render_template('query9.html', display = display,count = count)


if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
