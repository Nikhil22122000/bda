from typing_extensions import dataclass_transform
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import HashingVectorizer

data = pd.read_csv('spam_or_not_spam.csv')
dataArray = np.array(data)

bitArray = np.zeros(10000)
constant = 10000

def calcHashAndInsertInBitArray(wordVectors, bitArray):
    for i in range(wordVectors.shape[0]):
        hashVal1 = (wordVectors[i][0] * constant) % len(bitArray)
        hashVal2 = (wordVectors[i][1] * constant) % len(bitArray)
        hashVal3 = (wordVectors[i][2] * constant) % len(bitArray)
        #set bits in the bit array for the 3 hash functions
        bitArray[int(hashVal1)] = 1
        bitArray[int(hashVal2)] = 1
        bitArray[int(hashVal3)] = 1


def calcHashAndCheckForSpam(label0):
    wordVectors = createWordVectors(label0).toarray()

    falsePositive = 0
    for i in range(wordVectors.shape[0]):
        hashVal1 = (wordVectors[i][0] * constant) % len(bitArray)
        hashVal2 = (wordVectors[i][1] * constant) % len(bitArray)
        hashVal3 = (wordVectors[i][2] * constant) % len(bitArray)
        
        if(bitArray[int(hashVal1)] == 1 and bitArray[int(hashVal2)] == 1 and bitArray[int(hashVal3)] == 1):
            falsePositive += 1

    return falsePositive


def createWordVectors(data):
    vectorizer = HashingVectorizer(n_features=3)
    wordVectors = vectorizer.fit_transform(data.astype('U'))
    return wordVectors

def addToBloomsFilter(label1):
    wordVectors = createWordVectors(label1)
    calcHashAndInsertInBitArray(wordVectors.toarray(), bitArray)
    

label1 = [] #for spam
label0 = [] #for not spam
for i in range(len(dataArray)):
    if(dataArray[i][1] == 1):
        label1.append(dataArray[i][0])
    else:
        label0.append(dataArray[i][0])

label1 = np.array(label1)
label0 = np.array(label0)

addToBloomsFilter(label1)
falsePositive = calcHashAndCheckForSpam(label0)

print("Number of false positives = ", falsePositive)
print("Number of testing samples = ", len(label0))
print("False Positive Rate = ", falsePositive/len(label0))






