from calcFeatures import calc
from stanfordNER import labelEmail

from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.tag.stanford import NERTagger

import os
import sys
import json

def encode(inDir="./data", outDir="./labeled"):
    emails = []
    for file in os.listdir(inDir):
        if file.endswith(".txt"):
            email = labelEmail(os.path.join(inDir, file))
            email = json.dumps(email)
            emails.append(email)

    emails = "\n".join(emails)
    outFileName = "LabeledEmails.txt"
    with open(os.path.join(outDir,outFileName),'w') as fout:
        fout.write(emails)

def decode(filepath):
    """
    Decode emails
        Each line in file representes one email.
        A email is list of sentence.
        Sentence is list of tuple of [('word_token', ['feature',...], 'label'), ...,[...]]
    """
    with open(filepath) as fin:
        emails = fin.readlines()
        emails = [email.rstrip("\r\n") for email in emails]
        emails = [email.replace("ORGANIZATION", 'O') for email in emails]
        emails = [email.replace("PERSON", 'O') for email in emails]
        emails = [email.replace("MONEY", 'O') for email in emails]
        emails = [email.replace("PERCENT", 'O') for email in emails]
        emails = [json.loads(email) for email in emails]
        return emails

def formatEmail(email):
    formattedText = ""
    WordText = []   # text output for each word, features separated by space
    for sentence in email:
        sentence[0][1].append("FIRST")  # featrue indicate first word of sentence
        for word in sentence:
            features = " ".join(word[1])
            WordText.append(" ".join([word[0], features, word[2]]))
    return "\n".join(WordText)

def recomputeFeature(filepath):
    """
    RecomputeFeature for a data in a file
    """

    print "recomputing feature for '%s'"%filepath

    newEmails = []
    emails = decode(filepath)
    for email in emails:
        newEmail = []
        for sentence in email:
            tokenized_sentence = [w for w, f, l in sentence]
            features = calc(tokenized_sentence)
            newSentence = [[sentence[i][0] , features[i], sentence[i][2]] for i in range(0, len(sentence))]
            newEmail.append(newSentence)
        newEmails.append(newEmail)

    return newEmails

def recompute(inDir='./labeled', outDir='HMMinput'):
    """
    Recompute features for data of files in 'inDir'.
    Output the results for each email in separate files.
    """
    for file in os.listdir(inDir):
        if file.endswith(".txt"):
            emails = recomputeFeature(os.path.join(inDir, file))
            num=0;
            for email in emails:
                formattedTxt = formatEmail(email)
                with open(os.path.join(outDir, file[:-4]+"-%d.txt"%num), 'w') as fout:
                    fout.write(formattedTxt)
                num += 1

def recomputeUni(inDir, outDir, outFileName):
    """
    Recompute features for data of files in 'inDir'.
    Output the results combined into one file in 'outDir'.
    """
    out = []
    for file in os.listdir(inDir):
        if file.endswith(".txt"):
            out += recomputeFeature(os.path.join(inDir, file))

    formattedTxt = formatEmail(out)
    with open(os.path.join(outDir, outFileName), 'w') as fout:
        fout.write(formattedTxt)

def main(argv):
    inDir = argv[1]
    outDir = argv[2]
    encode(inDir,outDir)

if __name__ == '__main__':
    main(sys.argv)
