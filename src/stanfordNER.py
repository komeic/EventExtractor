from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.tag.stanford import NERTagger

import sys

st=NERTagger('./src/stanford-ner-2014-01-04/classifiers/english.muc.7class.distsim.crf.ser.gz','./src/stanford-ner-2014-01-04/stanford-ner.jar')

def getChunk(tagged_sentence):
    isCont = False
    res={"TIME":[], "DATE":[], "LOCATION":[]}
    chunk=""
    type=""
    for i in range(0,len(tagged_sentence)):
        if isCont==True and tagged_sentence[i][1]==type:
            chunk = chunk+" "+tagged_sentence[i][0]

        elif isCont==True:
            res[type].append(chunk)
            isCont=False

        elif tagged_sentence[i][1] in res.keys():
            isCont = True
            type = tagged_sentence[i][1]
            chunk=tagged_sentence[i][0]

    return res["TIME"],res["DATE"],res["LOCATION"]

def labelEmail(filepath):
    with open(filepath) as fin:
        content = fin.read()

    sentences = sent_tokenize(content)
    tokenized_sentences = [word_tokenize(sentence) for sentence in sentences]

    email =[st.tag(sentence) for sentence in tokenized_sentences]
    for i in range(0,len(email)):
        sentence = [[word[0], [], word[1]] for word in email[i]]    # insert empty features
        email[i] = sentence
    return email


if __name__ == '__main__':
    print labelEmail(sys.argv[1])

    # time=[]
    # date=[]
    # location=[]
    # for r in results:
    #     t,d,l = getChunk(r)
    #     time += t
    #     date += d
    #     location += l
    # print "Time: "+str(time)
    # print "Date: "+str(date)
    # print "Location: " + str(location)


