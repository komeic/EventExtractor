import redis, redisbayes
import sys
import os

rb = redisbayes.RedisBayes(redis=redis.Redis(host='localhost', port=6379, db=0))

def train(goodDir, badDir):
    count = 0
    for file in os.listdir(goodDir):
        if file.endswith(".train"):
            print "training %s" % file
            with open(os.path.join(goodDir, file), 'r') as fin:
                rb.train("event", fin.read().replace("\n", ""))
                count += 1
    count = 0
    for file in os.listdir(badDir):
        if file.endswith(".train"):
            print "training %s" % file
            with open(os.path.join(badDir, file), 'r') as fin:
                rb.train("nonevent", fin.read().replace("\n", ""))
                count += 1

def classify(filepath):
    dir,file = os.path.split(filepath)
    print "Classifying email: %s" % file
    with open(filepath, 'r') as fin:
        content = fin.read().replace("\n", "")
        result = rb.classify(content)
        return result

    return ""

def evaluate(goodDir, badDir):
    good = []
    for file in os.listdir(goodDir):
        if file.endswith(".test"):
            good.append([file, classify(os.path.join(goodDir, file))])

    tp=0
    for file, res in good:
        if res == "event":
            tp += 1
    tp = tp/len(good)
    fn = 1-tp

    bad = []
    for file in os.listdir(badDir):
        if file.endswith(".test"):
            bad.append([file, classify(os.path.join(badDir, file))])

    tn=0
    for file, res in good:
        if res == "nonevent":
            tn += 1
    tn = tp/len(good)
    fp = 1-tn

    result = good + bad
    print "result:"
    for file , res in result:
        print "%s: %s\n" %(file, res)
    print "tp: %f" % tp
    print "tn: %f" % tn
    print "fp: %f" % fp
    print "fn: %f" % fn

if __name__ == '__main__':

    if sys.argv[1] == "-d":
        train(sys.argv[2], sys.argv[3])
        classify('./data/classifier/good/07.test')
    else:
        train(sys.argv[1], sys.argv[2])
        evaluate(sys.argv[1], sys.argv[2])
