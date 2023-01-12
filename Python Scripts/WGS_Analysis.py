import re
import numpy as np
import pandas as pd
import csv
comment = r"""
#import file, setup lists
df = pd.read_csv(r"C:\Users\13144\Desktop\Analyzed.csv") 
print("Loaded")
print("Converting Columns to Binary")
#Importing the Analyzed Raw gave floats, so I'm just copying the code to create it from the original analyzed
List = {df.columns[0]:"Gene"}
for x in range(1,len(df.columns)):
    if re.search("ALS", df.columns[x]):
        List.update({df.columns[x]:1})
    else:
        List.update({df.columns[x]:0})
df = df.rename(columns=List) #this only can be renamed with lists
print("Computed")
#the data is integers in the lists. Need sums and frequencies for ALS and non ALS patients
sALS = [0]
sALS*=1112
snALS = sALS.copy()
fALS = sALS.copy()
fnALS = sALS.copy()

df =pd.read_csv(r"C:\Users\13144\Desktop\WGS_Analyzed_s&f.csv")
#Going row by row
print("Computing Sums & Frequencies")
for r in range(0,len(df)):
#first getting sum for each row, then dividing by length to get the frequency for each row
    print("Row " + str(r))
    for c in range(1,len(df.columns)):
        if df.iat[r,c] != 0:
            if df.columns[c]==0:
                sALS[r] +=1
            else:
                snALS[r] += 1
    fALS[r] = sALS[r]/(len(df.columns)-1)
    fnALS[r] = snALS[r]/(len(df.columns)-1)
print("Computed")
#setting up data columns so the data can be seen
df['sum_ALS'] = sALS
df['sum_nALS'] = snALS
df['frequency_ALS'] = fALS
df['frequency_nALS'] = fnALS
print("Sums & Frequency Columns assigned")
print("Saving")
#df.to_csv(r'C:\Users\13144\Desktop\WGS_Analyzed_s&f.csv')
print("Saved")"""
df =pd.read_csv(r"C:\Users\13144\Desktop\WGS_Analyzed_s&f.csv")
#need top to work first
c = 0
#I'm going to create a seperate dataframe for the joint probability
#loop for creating list for the indexes of tbe joint frequencies (vertical)
print("Creating Joint Frequency DataFrame")
l = []
for x in range(0,1112):
    a = "i" + str(x)
    l.append(a)
Lex = {"ALS Expected jf":l}
Lem = {"ALS Empirical jf":l}
Lnex = {"nALS Expected jf":l}
Lnem = {"nALS Empirical jf":l}
print("Generating Columns")
#loop for creating columns
# the dataframes need indices with unique names
for x in range(1, 1112):
    cola = "ia"+str(x)
    colb = "ib"+str(x)
    colc = "ic"+str(x)
    cold = "id"+str(x)
    Lex[cola] = [0]*1112
    Lem[colb] = [0]*1112
    Lnex[colc] = [0]*1112
    Lnem[cold] = [0]*1112
print("Generated")
#combining them into a big list
Ljp = {}
Ljp.update(Lex)
Ljp.update(Lem)
Ljp.update(Lnex)
Ljp.update(Lnem)
#creates the dataframe
dfjp = pd.DataFrame(Ljp)
print("DataFrame created")



x = 0
#doing nALS and ALS together is faster for empirical.
#a = 0 for exp ALS, 1 for emp (ALS & non ALS), 2 for exp non ALS
print("Computing Joint Frequencies")
columns = tuple(df.columns)
l = len(columns) - 5
sum = 0
nsum = 0
#recalculate empirical for one row
for a in range(0,3):
    #keeping this external should speed things up
    print(a)
    print(" ")
    nf = nsum / (l)
    f = sum / (l)
    #0 to 1111, 1 to 1111
    #joint probability should look like a half triangle for the data
    #row index starts from 0 and column starts from 1. column increases by 1 each time row increases by 1. cuts computation time in half
    for r in range(0,1112):#1111
        print("Row " + str(r))
        for c in range(r,1111): #1110
            if(1==2): #empirical
                print("c"+str(c))
                sum = 0
                nsum = 0
                for col in range(1,l+1): #compares each column
                    if df.iat[r,col] != 0 and df.iat[c+1,col] !=0:
                        if(columns[col]==1):
                            sum +=1
                        else:
                            nsum += 1
                dfjp.iat[ r,c+1112 ] = sum / l
                dfjp.iat[ r,c +3334 ] = nsum / l
            elif(a==0): #expected ALS
                x = df.iat[r,-2]+df.iat[c+1,-2]
                dfjp.iat[r,c+1] = x
            else: #expected non ALS
                x = df.iat[r,-1]+df.iat[c+1,-1]
                dfjp.iat[ r,c+2225 ] = x
#test
print(dfjp.head(1))
print("Joint Frequencies Computed")
print("Saving")
dfjp.to_csv(r'C:\Users\13144\Desktop\WGS_Analyzed_jp2.csv')
print("Saved")
