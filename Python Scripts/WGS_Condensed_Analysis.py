import pandas as pd
import numpy as np
import re
#I commented this because this part ran clean. This wastes too much time being repeated.
df = pd.read_csv(r"C:\Users\13144\Desktop\Data Analysis\WGS_Base File.csv")
df.set_index('Gene')
sdf = df.copy()
print("Loaded")
print("Creating condensed dataframe")
#remove everything but first 34 rows
#this is a workaround. It works. Don't touch it.
l = list(range(34,1112))
sdf.drop(l,axis=0,inplace = True)
print("Created")
print("Filling condensed Dataframe")
#set 1st column from 1 to 34
r = range(1,35)
sdf.iloc[:,0] = r
#find where the first of each gene starts in the rows
start = []
i = 0
for x in range(0,len(df)):
    if df.iat[x,0] > i:
        start.append(x)
        i+=1
#add end index to start so it doesn't go out of index when doing r+1 for last
start.append(1112)
start = tuple(start)
#compress the variants into genes
for c in range(1,len(df.columns)): #6000ish. don't include indexing columns
    print("Column" + str(c))
    for r in range(0,len(sdf)): #34
        sum = df.iloc[start[r]:start[r+1],c].sum()
        if sum==0:
            sdf.iat[r,c] = 0
        else:
            sdf.iat[r,c] = 1
print("Done")
print("Converting headers to binary")
#convert headers to binary
List = {sdf.columns[0]:"Gene"}
for x in range(1,len(sdf.columns)):
    if re.search("ALS", sdf.columns[x]):
        List.update({sdf.columns[x]:1})
    else:
        List.update({df.columns[x]:0})
sdf = sdf.rename(columns=List) #this only can be renamed with lists

print("Computing sums and frequencies")
#finds sums and frequencies of list
#need to not count the 'index' column
List.pop(sdf.columns[0])
values = np.array( list(List.values()) )
zeroes = list(np.where(values==0)[0])
ones = list(np.nonzero(values)[0])
sALS = [0]
sALS*=34
sCtr = sALS.copy()
fALS = sALS.copy()
fCtr = sALS.copy()
for r in range(0,len(sdf)):
    sALS[r] = sdf.iloc[r,ones].sum()
    sCtr[r] = sdf.iloc[r,zeroes].sum()
    fALS[r] = sALS[r]/len(sdf.columns)
    fCtr[r] = sCtr[r]/len(sdf.columns)
print("Done")
#setting up data columns for sum & frequency
sdf['sum_ALS'] = sALS
sdf['sum_Ctr'] = sCtr
sdf['frequency_ALS'] = fALS
sdf['frequency_Ctr'] = fCtr
sdf.set_index('Gene')
print("Saving")
sdf.to_csv(r"C:\Users\13144\Desktop\Data Analysis\Gene Analysis\Probability\WGS_GeneAnalyzed_s&f.csv")
print("Saved")



#copy & paste amirite
#I'm going to create a seperate dataframe for the joint probability
#loop for creating list for the indexes of tbe joint frequencies (vertical)
#from gene 1 to gene 34. I'm too lazy to change some of the names
print("Creating Joint Frequency DataFrame")
l = []
for x in range(1,35):
    a = "g" + str(x)
    l.append(a)
Lex = {"ALS Expected jf":l}
Lem = {"ALS Empirical jf":l}
Lnex = {"Ctr Expected jf":l}
Lnem = {"Ctr Empirical jf":l}
print("Generating Columns")
#loop for creating columns
#needs to be done for each dataframe
for x in range(2, 35):
    col = "g"+str(x)
    Lex[col] = [0]*34
    Lem[col] = [0]*34
    Lnex[col] = [0]*34
    Lnem[col] = [0]*34
print("Generated")
#create dataframes
dfjpExp = pd.DataFrame(Lex)
dfjpEmp = pd.DataFrame(Lem)
dfjpCExp = pd.DataFrame(Lnex)
dfjpCEmp = pd.DataFrame(Lnem)
dfjpEmp.set_index("ALS Empirical jf")
dfjpExp.set_index("ALS Expected jf")
dfjpCEmp.set_index("Ctr Empirical jf")
dfjpCExp.set_index("Ctr Expected jf")
#creates the dataframe
print("DataFrames created")


print("Calculating Joint Frequencies")
x = 0
#doing nALS and ALS together is faster for empirical.
#a = 0 for empirical(both), 1 for expected(ALS), 2 for for expected control 
#This should be a hell of a lot fast doing them all at once vs one at a time
print("Computing Joint Frequencies")
columns = tuple(sdf.columns)
l = len(columns) - 5
#recalculate empirical for one row
for a in range(0,3):
    #keeping this external should speed things up
    print(a)
    print(" ")
    #0 to 1111, 1 to 1111
    #joint probability should look like a half triangle for the data
    #row index starts from 0 and column starts from 1. column increases by 1 each time row increases by 1. cuts computation time in half
    for r in range(0,34):#34
        print("Row " + str(r))
        for c in range(r+1,34): #row +1 to 34. starts at least at 1
            if(a==0): #Empirical
                #Average for loop comparison fan vs average set comparison enjoyer
                dfjpEmp.iat[ r,c ] = len(   set( sdf.iloc[r,ones].to_numpy().nonzero()[0] ) & set( sdf.iloc[c,ones].to_numpy().nonzero()[0] )   ) / l #ALS
                dfjpCEmp.iat[ r,c ] = len(   set( sdf.iloc[r,zeroes].to_numpy().nonzero()[0] ) & set( sdf.iloc[c,zeroes].to_numpy().nonzero()[0] )   ) / l #Control
            elif(a==1): #Expected ALS
                x = sdf.iat[r,-2]*sdf.iat[c,-2]
                dfjpExp.iat[r,c] = x
            else: #expected Control
                x = sdf.iat[r,-1]*sdf.iat[c,-1]
                dfjpCExp.iat[ r,c ] = x
print("Joint Frequencies Computed")
#drop index columns
print("Saving")
dfjpEmp.to_csv(r"C:\Users\13144\Desktop\Data Analysis\Gene Analysis\Probability\WGS_GeneAnalyzed_AEmp.csv")
dfjpExp.to_csv(r"C:\Users\13144\Desktop\Data Analysis\Gene Analysis\Probability\WGS_GeneAnalyzed_AExp.csv")
dfjpCEmp.to_csv(r"C:\Users\13144\Desktop\Data Analysis\Gene Analysis\Probability\WGS_GeneAnalyzed_CEmp.csv")
dfjpCExp.to_csv(r"C:\Users\13144\Desktop\Data Analysis\Gene Analysis\Probability\WGS_GeneAnalyzed_CExp.csv")
print("Saved")