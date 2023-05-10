from numpy import number
import pandas as pd

data = pd.read_csv('./countingOnes.csv')
stream = data['Stream']
print('data stream')
print(stream)

def createBuckets(stream):
    bucket_list = []

    current_power = 0
    current_timestamp = 0
    counter = 0
    current_bucket = []
    number_of_ones = 0
    
    for i in range(len(stream)-1, 0, -1):

        if(len(current_bucket) == 0):
            if(stream[i] == 1):
                current_bucket.append(stream[i])
                current_timestamp = i
                number_of_ones += 1
        elif(number_of_ones < 2**current_power):
            if(stream[i] == 1):
                number_of_ones += 1
            current_bucket.append(stream[i])

        if(number_of_ones >= 2**current_power):
            bucket_list.append([number_of_ones, current_timestamp])
            current_bucket = []
            current_timestamp = 0
            counter += 1
            number_of_ones = 0
            if(counter >= 2):
                counter = 0
                current_power += 1
    
    return bucket_list


bucket_list = createBuckets(stream)
print('List of buckets formed =', bucket_list)

def answerQuery(timestamp):     #number of ones after timestamp 14

    number_of_ones = 0

    for i in range(len(bucket_list)):
        if(bucket_list[i][1] > timestamp):
            number_of_ones += bucket_list[i][0]
        else:
            number_of_ones += bucket_list[i][0] / 2
            break

    return number_of_ones

k = 14
print('Number of 1s after timestamp', k, '=', answerQuery(k))

