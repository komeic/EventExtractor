from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

import os
import sys
import json
stopword = [".", "?", "!", "\n"]

def preprocess(content):
    processed = []
    for line in content:
        if len(line)==1 and line[0]=="\n":
            continue
        if not line[-1] in stopword:
            line=line[:-1]+"."
        line = line.replace("/", " / ")
        line = line.replace("(", "( ")
        line = line.replace(")", " )")
        line = line.replace("  ", " ")
        processed.append(line)
    processed = "".join(processed)
    return processed

def labelEmail(filepath):

    print "Preprocessing file: %s" % (filepath)
    with open(filepath) as fin:
        # content = fin.read()
        content = fin.readlines()[1:]
        content = preprocess(content)

    sentences = sent_tokenize(content)
    tokenized_sentences = [word_tokenize(sentence) for sentence in sentences]

    email = []
    for sentence in tokenized_sentences:
        formatted = [[word, [], "UNKNOWN"] for word in sentence]    # insert empty features
        email.append(formatted)
    print "Completed preprocessing.\n"
    return email

def encode(inDir="./data", outDir="./labeled"):
    emails = []
    count = 0
    num = 0
    for file in os.listdir(inDir):
        if file.endswith(".txt"):
            if count == 10:
                count=0
                num+=1
                emails = "\n".join(emails)
                outFileName = "LabeledEmails0%d.txt"%num
                filepath = os.path.join(outDir,outFileName)
                while os.path.exists(filepath):
                    num+=1
                    outFileName = "LabeledEmails0%d.txt"%num
                    filepath = os.path.join(outDir,outFileName)
                with open(filepath,'w') as fout:
                    fout.write(emails)
                emails = []
            email = labelEmail(os.path.join(inDir, file))
            email = json.dumps(email)
            emails.append(email)
            count += 1

    if len(emails) != 0:
        emails = "\n".join(emails)
        outFileName = "LabeledEmails0%d.txt"%num
        filepath = os.path.join(outDir,outFileName)
        while os.path.exists(filepath):
            num+=1
            outFileName = "LabeledEmails0%d.txt"%num
            filepath = os.path.join(outDir,outFileName)
        with open(filepath,'w') as fout:
            fout.write(emails)
            emails = []

if __name__ == '__main__':
    argv = sys.argv
    encode(argv[1],argv[2])
