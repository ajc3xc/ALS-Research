import re
import numpy as np
import pandas as pd
import csv
#import file, setup dictionaries
df = pd.read_csv(r"C:\Users\13144\Documents\Gene_Analysis_Shortened.csv") 
print("Loaded")
numbers = {r"'0/0":0,r"'./.":0,r"'0/1":1,r"'1/1":2,r"'0/2":2,r"'1/2":3,r"'2/2":4,r"'0/3":3,r"'2/1":3,r"'0/3":3,r"'2/3":5,r"'0/4":4,r"'2/4":6,"'3/3":6}
genes = {"NDC1":1,"TPR":2,"LBR":3,"NUP133":4,"AHCTF1":5,"SEC13":6,"NUP210":7,"CHMP2B":8,"NUP54":9,"NUP155":10,"NUP153":11,"LEMD2":12,"SUN1":13,"POM121":14,"NUP205":15,"CHMP4C":16,"GLE1":17,"NUP188":18,"NUP214":19,"NUP98":20,"NUP160":21,"NXF1":22,"LEMD3":23,"NUP107":24,"NUP58":25,"CHMP4A":26,"VPS4A":27,"IST1":28,"NUP88":29,"KPNB1":30,"SEH1L":31,"VPS4B":32,"CHMP2A":33,"RANGAP1":34}

#Test
#for x in range(0,len(df["Gene"])):
 #   y = re.sub(df.iloc[x][0],str(genes[df.iloc[x][0]]),df.iloc[x][0])
  #  df['Gene'][x] = y
#print(df["Gene"][:5])
#The actual computation
flag = True
print("Computing")
for c in range(0,len(df.columns)):
    print("Column " + str(c))
    for r in range(0,len(df)):
        if flag:
            a = re.sub(df.iloc[r][0],str(genes[df.iloc[r][0]]),df.iloc[r][0])
            df.iloc[r][0] = a
        else:
            a = re.sub(df.iloc[r][c],str(numbers[df.iloc[r][c]]),df.iloc[r][c])
            df.iloc[r][c] = a
    flag = False
print("Computed")
df.to_csv(r'C:\Users\13144\Desktop\Analyzed.csv')
print("Saved")