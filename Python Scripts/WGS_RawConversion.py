import modin.pandas as pd
import ray
ray.init()
import numpy as np
import re


#Load file
print("Loading")
df = pd.read_csv(r"C:\Users\13144\Desktop\Data Analysis\WGS2\WGS2_BaseFile.csv")

dfDominant = df.copy()
dfRecessive = df.copy()

#create dictionaries
dictDom = {r"'./.":0}
dictRec = {r"'./.":0}

#set dictionary
MAX = 10;
print("Creating cell dictionary")
for x in range(0,MAX):
    for y in range(0,MAX):
        dNum = 0
        rNum = 0
        if x>0:
            dNum = 1
            if y>0:
                rNum = 1
        if y>0:
            dNum = 1;
        dictDom[r"'" +str(x)+ "/" +str(y)] = dNum
        dictRec[r"'" +str(x)+ "/" +str(y)] = rNum
            
                
            
print("Done")

#convert dataframe cells
print("Converting cells")
dfDominant.iloc[:,1:]= dfDominant.iloc[:,1:].replace(dictDom)
dfRecessive.iloc[:,1:]= dfRecessive.iloc[:,1:].replace(dictRec)
print("Converted")

#Convert dataframe headers to binary
print("Converting headers")
dictHead = {df.columns[0]:"Gene"}
for x in range(1,len(df.columns)):
    if re.search("ALS", df.columns[x]):
        dictHead.update({df.columns[x]:1})
    else:
        dictHead.update({df.columns[x]:0})
dfDominant = dfDominant.rename(columns=dictHead)
dfRecessive = dfRecessive.rename(columns=dictHead)
print("Converted")

#convert gene names to numbers
print("Converting index titles to  numbers")
geneNames = list(df['Gene'].unique())
genes = len(geneNames)
geneValues = list(range(1,genes+1))
dictIndex = dict(zip(geneNames,geneValues))
print(dictIndex)
dfDominant.iloc[:,0] = dfDominant.iloc[:,0].replace(dictIndex)
dfRecessive.iloc[:,0] = dfRecessive.iloc[:,0].replace(dictIndex)
print("Titles converted")
print(df)
#print("Done")




print("Saving")
dfDominant.to_csv(r"C:\Users\13144\Desktop\Data Analysis\WGS2_Dominant.csv")
dfRecessive.to_csv(r"C:\Users\13144\Desktop\Data Analysis\WGS2_Recessive.csv")
print("Saved")
