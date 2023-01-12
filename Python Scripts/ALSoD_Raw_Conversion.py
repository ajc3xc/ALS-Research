import modin.pandas as pd
import ray
ray.init()
import numpy as np
import re


#Load file
print("Loading")
df = pd.read_csv(r"C:\Users\13144\Desktop\Data Analysis\ALSoD2\ALSoD2_Raw.csv")

#create dictionary
dictCell = {r"'./.":0}
MAX = 10;
print("Creating cell dictionary")
for x in range(0,MAX):
    for y in range(0,MAX):
        dictCell[r"'" +str(x)+ "/" +str(y)] = x+y
print("Done")

#convert dataframe cells
print("Converting cells")
df.iloc[:,1:]=df.iloc[:,1:].replace(dictCell)
print("Converted")

#Convert dataframe headers to binary
print("Converting headers")
dictHead = {df.columns[0]:"Gene"}
for x in range(1,len(df.columns)):
    if re.search("ALS", df.columns[x]):
        dictHead.update({df.columns[x]:1})
    else:
        dictHead.update({df.columns[x]:0})
df = df.rename(columns=dictHead)
print("Converted")

#convert gene names to numbers
print("Converting index titles to  numbers")
geneNames = list(df['Gene'].unique())
genes = len(geneNames)
geneValues = list(range(1,genes+1))
dictIndex = dict(zip(geneNames,geneValues))
print(dictIndex)
df.iloc[:,0] = df.iloc[:,0].replace(dictIndex)
print("Titles converted")
print(df)
#print("Done")




print("Saving")
df.to_csv(r"C:\Users\13144\Desktop\Data Analysis\ALSoD2\ALSoD2_Sum.csv")
print("Saved")
