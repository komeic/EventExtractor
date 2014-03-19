import nltk
from nltk.tag.simplify import simplify_wsj_tag

import re
import sys

################### Dictionaries #######################
_DateDict = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
             "mon", "tue", "wed", "thu", "fri", "sat", "sun", "tomorrow", "yesterday"]
_MonthDict = ["january", "february", "march", "april", "may", "june",
              "july", "august", "september", "october", "november", "december"
              "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
DayDict = _DateDict + _MonthDict
LocationDict = ["Boelter", "Hall", "BH", "Young", "Dashew", "Center", "Career", "Strathmore", "Westwood",
            "Student", "Activities","Center", "Murphy", "Humanities",
            "building", "Building", "room", "Room"]
SpecialChar = ["/", "-", ",", ":"]
########################################################

################### Feature Names ######################
CAPITAL = "CAPITAL"
NOUN = "NOUN"
PRONOUN = "PRONOUN"
PREP = "PREP"
NUM = "NUM"
DICT_DATE = "DATE"
TIME = "TIME"
LOC = "LOC"
SPECIAL = "SPECIAL"
########################################################

def getPOS(tokenized_sentence):
    tagged_sent = nltk.pos_tag(tokenized_sentence)
    simplified = [simplify_wsj_tag(tag) for word, tag in tagged_sent]
    return simplified

def isCap(tokenized_sentence, i):
    if tokenized_sentence[i]=="":
        return False
    return tokenized_sentence[i][0].isupper()

def isNum(tokenized_sentence, pos, i):
    if pos[i] == "NUM":
        return True
    elif re.match(r".*?\d{1,6}.*$", tokenized_sentence[i]):
        return True
    else:
        return False

def isNoun(pos, i):
    if pos[i] == "N":
        return True
    else:
        return False

def isProNoun(pos, i):
    if pos[i] == "NP":
        return True
    else:
        return False

def isPrep(pos, i):
    if pos[i] == "P":
        return True
    else:
        return False

def isDate(tokenized_sentence, i):
    if tokenized_sentence[i].lower() in DayDict:
        return True
    else:
        return False

def isTime(tokenized_sentence, i):
    if "am" in tokenized_sentence[i].lower():
        return True
    if "pm" in tokenized_sentence[i].lower():
        return True
    if re.search(r"\d:\d\d", tokenized_sentence[i]):
        return True
    return False

def isLoc(tokenized_sentence, i):
    if tokenized_sentence[i] in LocationDict:
        return True
    else:
        return False

def isSpecial(tokenized_sentence, i):
    if len(tokenized_sentence[i])==1 and tokenized_sentence[i] in SpecialChar:
        return True
    return False

def calc(tokenized_sentence):
    pos = getPOS(tokenized_sentence)
    features = []
    for i in range(0,len(tokenized_sentence)):
        feature = []
        if isCap(tokenized_sentence, i):
            feature.append(CAPITAL)
        if isNum(tokenized_sentence, pos, i):
            feature.append(NUM)
        if isNoun(pos, i):
            feature.append(NOUN)
        if isProNoun(pos, i):
            feature.append(PRONOUN)
        if isPrep(pos, i):
            feature.append(PREP)
        if isDate(tokenized_sentence, i):
            feature.append(DICT_DATE)
        if isTime(tokenized_sentence, i):
            feature.append(TIME)
        if isLoc(tokenized_sentence, i):
            feature.append(LOC)
        if isSpecial(tokenized_sentence, i):
            feature.append(SPECIAL)
        features.append(feature)

    return [features[i] for i in range(0, len(features))]

def main():
    pass

if __name__ == '__main__':
    main()
