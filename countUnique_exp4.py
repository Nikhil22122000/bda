import pandas as pd

data = pd.read_csv('./uniqueElements.csv')
stream = data['Elements']
print('data stream ')
print(stream)

maxnum=0
for i in range(0,len(stream)):
    #ax+b mod c
    val= bin((1*stream[i] + 6) % 32)[2:]
    
    sum=0
    for j in range(len(val)-1,0,-1):
        
        if val[j]=='0':
            sum+=1
        else:
            break
    if sum>maxnum:
        maxnum=sum

print('distict elements ', 2**maxnum)


