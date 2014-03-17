from calcFeatures import calc

from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.tag.stanford import NERTagger

import sys

st=NERTagger('/Users/honghong_chen/Dropbox/CS/cs263a/project/stanford-ner-2014-01-04/classifiers/english.muc.7class.distsim.crf.ser.gz','/Users/honghong_chen/Dropbox/CS/cs263a/project/stanford-ner-2014-01-04/stanford-ner.jar')



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

def main():
    pass


if __name__ == '__main__':
    args = sys.argv
    with open(args[1]) as f:
        content = f.read()

    sentences = sent_tokenize(content)
    tokenized_sentences = [word_tokenize(sentence) for sentence in sentences]

    features = [calc(sentence) for sentence in tokenized_sentences]
    for f in features:
        print f

    # results=[st.tag(sentence) for sentence in tokenized_sentences]

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


