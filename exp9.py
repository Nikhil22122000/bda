from bs4 import BeautifulSoup
import requests
import numpy as np


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


def answerQuery(timestamp, bucket_list):     #number of ones after timestamp 14

    number_of_ones = 0

    for i in range(len(bucket_list)):
        if(bucket_list[i][1] > timestamp):
            number_of_ones += bucket_list[i][0]
        else:
            number_of_ones += bucket_list[i][0] / 2
            break

    return number_of_ones

k = 14
print('Number of likes after timestamp', k, '=', answerQuery(k))


def get_rating(soup):
    try:
        rating = soup.findAll("i", {'data-hook':'review-star-rating'})
    except AttributeError:
        try:
            rating = soup.findAll("span", {'class':'a-icon-alt'}).string.strip()
        except:
            rating = ""	
    
    return rating


if __name__ == "__main__":

    HEADERS = ({'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                'Accept-Language': 'en-US, en;q=0.5'})

    links = ["https://www.amazon.com/Sony-PlayStation-Pro-1TB-Console-4/product-reviews/B07K14XKZH/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber=1",
            "https://www.amazon.com/dp/B0B9T3Y3VM/ref=syn_sd_onsite_desktop_0?ie=UTF8&pf_rd_p=0b99589b-9e53-4dcd-9ac5-fe5c7519bedd&pf_rd_r=FN45Q7S4YA1R29A68F5W&pd_rd_wg=QWfMb&pd_rd_w=qU9RG&pd_rd_r=59bb87cd-38ab-43b6-baff-8d607b8e12fc&th=1"
            ]
    
    for link in links:
        URL = link 
        # print(URL)
        webpage = requests.get(URL, headers=HEADERS)

        soup = BeautifulSoup(webpage.content, "lxml")
        rating = get_rating(soup)
        print("Product Rating =", np.shape(rating))
        print()
        createBuckets(rating)


        


