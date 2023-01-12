import re
import pandas as pd
import numpy
import csv
df = pd.read_csv(r"C:\Users\13144\Desktop\Analyzed.csv") 
print("Loaded")
print("Computing")
#It was too hard directly assigning, so I used a dictionary
List = {df.columns[0]:"Gene"}
for x in range(1,len(df.columns)):
    if re.search("ALS", df.columns[x]):
        List.update({df.columns[x]:1})
    else:
        List.update({df.columns[x]:0})
df = df.rename(columns=List)
#print(df.columns[:5])
print("Finished")
df.to_csv(r'C:\Users\13144\Desktop\Analyzed2.csv')
print("Saved")
