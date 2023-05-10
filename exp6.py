import pandas as pd
import numpy as np

data = pd.read_csv('./Test_data.csv')
source_ip_addr = data['src_bytes']
vulnerable_windows = 0

#FM algorithm
window_size = 100
#len(source_ip_addr)
total_windows = 0
for k in range(0, 1000 - window_size + 1):
    total_windows += 1
    maxnum=0
    for i in range(0, window_size):

        #ax+b mod c
        val= (15*source_ip_addr[i] + 25) % 111
        bin_val = bin(val)[2:]
        # print(val)
        sum=0
        #trailing zeros 
        for j in range(len(bin_val)-1,0,-1):
            
            if bin_val[j]=='0':
                sum+=1
            else:
                break
        if sum>maxnum:
            maxnum=sum

    distinct_elements = 2**maxnum

    #check for spam windows
    if(distinct_elements < 20):
        vulnerable_windows += 1
    
print("Windows with possiblity of attack = ", vulnerable_windows)


