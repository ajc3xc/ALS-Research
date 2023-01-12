import pandas as pd
#import ray
#ray.init()
import numpy as np
import re

print("Loading")
#setup files, create sets
ldf = pd.read_csv(r"C:\Users\13144\Desktop\Data Analysis\WGS_Variant_Report_Raw.csv")
ldf = ldf.set_index("Gene")
rdf = ldf.copy()
df = ldf.to_numpy()
zeroes = np.argwhere(df==r"'0/0")
periods = np.argwhere(df==r"'./.")
zeroes = np.concatenate(zeroes,periods)
zeroes = [tuple(x) for x in zeroes]
zeroes = set(zeroes)
allCrds = np.argwhere(df != 0)
nonzeroes = allCrds - zeroes
allCrds = tuple(allCrds)
nonzeroes = tuple(nonzeroes)

for crd in zeroes:
    ldf.iat[crd[0],crd[1]] = 0
    rdf.iat[crd[0],crd[1]] = 0

left1 = np.argwhere(df)


#do data wrangling, save
print("Wrangling Data")
for r in range(0,len(ldf)):
    print("Row "+str(r))#Show row being computed
    for c in range(0,len(ldf.columns)):
        print("Column "+str(c))
        crd = numbers[ldf.iat[r,c]]
        ldf.iat[r,c]=crd[0]#left
        rdf.iat[r,c]=crd[1]#right
print("Done")

print("Saving")
ldf.to_csv(r"C:\Users\13144\Desktop\Data Analysis\WGS_PairLeft_Raw.csv")
rdf.to_csv(r"C:\Users\13144\Desktop\Data Analysis\WGS_PairRight_Raw.csv")
print("Saved")