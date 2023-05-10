import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori, association_rules

df = pd.read_csv('./groceries1.csv')
arr = np.array(df)

def findFreqItemSets(idx):
  uniqueItems = set()

  for i in range(idx, idx+100):
    for j in range(1, int(arr[i][0] + 1)):
      uniqueItems.add(arr[i][j])

  uniqueItems = list(uniqueItems)

  items_list = []
  for i in range(1, 101):
    items = []
    for j in range(len(uniqueItems)):
      if uniqueItems[j] in arr[i]:
        items.append(1)
      else:
        items.append(0)
    items_list.append(items)

  item_df = pd.DataFrame(items_list)

  freq_item_sets = apriori(item_df, min_support = 0.05, use_colnames=True)
  return freq_item_sets, uniqueItems

freqItemSets = []
for idx in range(0, len(arr)-100, 100):
  freq, uniqueItems = findFreqItemSets(idx)
  for i in freq.index:
    if(len(freq['itemsets'][i]) > 1):
      items = []
      for itemIdx in freq['itemsets'][i]:
         items.append(uniqueItems[itemIdx])
      freqItemSets.append(items)

print(freqItemSets)