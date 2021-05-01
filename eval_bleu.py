import nltk
import random
from scipy import stats
import pickle

#data_name = "cotra"
vocab_file = "data/chars.pkl"
vocab = pickle.load(open(vocab_file, 'rb'))
vocab.append(' ')
pad = vocab.index(' ')


reference_file = "data/reference_file.txt"
hypothesis_file_leakgan = "data/generated_file.txt"

#######################################################

reference = []
with open(reference_file) as fin:
    for line in fin:
        candidate = []
        line = line.split()
        for i in line:
            if i == str(pad):
                break
            candidate.append(i)
    reference.append(candidate)

#######################################################

hypothesis_list_leakgan = []
with open(hypothesis_file_leakgan) as fin:
    for line in fin:
        line = line.split()
        while line[-1] == str(pad):
            line.remove(str(pad))
        hypothesis_list_leakgan.append(line)

#######################################################
#######################################################
random.shuffle(hypothesis_list_leakgan)
#######################################################
#Now the bleu evaluation starts
from nltk.translate.bleu_score import SmoothingFunction
smoothie = SmoothingFunction().method4
for ngram in range(2, 6):
    weight = tuple((1. / ngram for _ in range(ngram))) #weight of certain bleu score is 1/N
    bleu_leakgan = []
    bleu_supervise = []
    bleu_base2 = []
    num = 0
    for h in hypothesis_list_leakgan[:2000]:
        BLEUscore = nltk.translate.bleu_score.sentence_bleu(reference, h, weight, smoothing_function=smoothie)
        #print(num, BLEUscore)
        num += 1
        bleu_leakgan.append(BLEUscore)
    print("LeakGAN")
    print(len(weight), "-gram BLEU score: ", 1.0 * sum(bleu_leakgan)/len(bleu_leakgan)) # average

pickle.dump([hypothesis_list_leakgan], open("data/significance_test_sample.pkl", "wb"))
