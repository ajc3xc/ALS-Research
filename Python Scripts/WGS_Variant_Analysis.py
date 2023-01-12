#modin should make things faster
import pandas as pd
import numpy as np
import re
#basically recreate joint probability using a different, faster method

df = pd.read_csv(r"C:\Users\13144\Desktop\Data Analysis\WGS_Base File.csv")
print("Converting headers to binary")

#convert headers to binary numbers. store w/ dictionary
List = {df.columns[0]:"Gene"}
for x in range(1,len(df.columns)):
    if re.search("ALS", df.columns[x]):
        List.update({df.columns[x]:1})
    else:
        List.update({df.columns[x]:0})
df = df.rename(columns=List) #this only can be renamed with a dictionary / list / tuple

print("Computing sums and frequencies")
#finds sums and frequencies of list
#need to not count the 'index' column auto generated
#finds where the columns are 0 and nonzero. used later
#uses list storing zero and non zero values for array
values = np.array( list(List.values()) )
cvalues = values.copy()
ones = list(np.nonzero(values)[0])#same as above
zeroes = arange(1,len(df.columns))
for x in ones:
    zeroes.remove(

print(zeroes[:100])
print(" ")
print(ones)
exit()
sALS = [0]
sALS*=len(df)
sCtr = sALS.copy()
fALS = sALS.copy()
fCtr = sALS.copy()
for r in range(0,len(df)):
    sALS[r] = df.iloc[r,ones].sum()
    sCtr[r] = df.iloc[r,zeroes].sum()
    fALS[r] = sALS[r]/len(df.columns)
    fCtr[r] = sCtr[r]/len(df.columns)
print("Done")
#setting up data columns for sum & frequency
df['sum_ALS'] = sALS
df['sum_Ctr'] = sCtr
df['frequency_ALS'] = fALS
df['frequency_Ctr'] = fCtr
df.set_index('Gene',inplace=True,drop=True)
print("Saving")
df.to_csv(r"C:\Users\13144\Desktop\Data Analysis\Variant Analysis\Joint Probability\WGS_VariantAnalysis_S&F")
print("Saved")



#copy & paste amirite
#I'm going to create a seperate dataframe for the joint probability
print("Creating Joint Frequency DataFrame")
l = []
for x in range(0,len(df)):
    a = "i" + str(x)
    l.append(a)
Lex = {"ALS Expected jf":l}
Lem = {"ALS Empirical jf":l}
Lnex = {"Ctr Expected jf":l}
Lnem = {"Ctr Empirical jf":l}
print("Generating Columns")
#loop for creating columns
#needs to be done for each dataframe
for x in range(1, len(df)):
    col = "i"+str(x)
    Lex[col] = [0]*len(df)
    Lem[col] = [0]*len(df)
    Lnex[col] = [0]*len(df)
    Lnem[col] = [0]*len(df)
print("Generated")
#create dataframes
dfjpExp = pd.DataFrame(Lex)
dfjpEmp = pd.DataFrame(Lem)
dfjpCExp = pd.DataFrame(Lnex)
dfjpCEmp = pd.DataFrame(Lnem)
#creates the dataframe
print("DataFrames created")



print("Finding nonzero coordinates")

#seperate into ALS and control columns
dfCtr = df.iloc[:,zeroes]
dfALS = df.iloc[:,ones]
#find nonzero coordinate
dfALS = dfALS.to_numpy()
dfALS = np.transpose(np.nonzero(dfALS))
print(len(dfALS))
dfCtr = dfCtr.to_numpy()
data = np.transpose(np.nonzero(dfCtr))
print(len(dfCtr))
exit()

#convert to list of tuples
dfALS = dfALS.tolist()
dfCtr = dfCtr.tolist()
dfALS = [tuple(x) for x in dfALS]
dfCtr = [tuple(x) for x in dfCtr]

#save them into a list of sets of tuples of the coordinates, by row
ALSNonZero = [0]*len(df)
CtrNonZero = [0]*len(df)
print("Found")

print("Converting to list of nonzeroes for each row")
for i in range(0,len(df)):
    ALSNonZero[i] = set([item for item in dfALS if item[0]==x])
    CtrNonZero[i] = set([item for item in dfCtr if item[0]==x])
#convert to tuples for faster speed reading
ALSNonZero = tuple(ALSNonZero)
print("ALS and Control lengths")
print(len(ALSNonZero[5]))
CtrNonZero = tuple(CtrNonZero)
print(len(CtrNonZero[5]))
print("Finished")
exit()







#Should make 4x faster
import modin.pandas as pd
#If a bigger dataframe is used then modin will be needed, but in this case it works fine for jp.
print("Calculating Joint Frequencies")
x = 0
#doing nALS and ALS together is faster for empirical.
#a = 0 for empirical(both), 1 for expected(ALS), 2 for for expected control 
#This should be a hell of a lot fast doing them all at once vs one at a time like I used to.
print("Computing Joint Frequencies")
columns = tuple(df.columns)
l = len(columns) - 4
#recalculate empirical for one row
for a in range(0,3):
    #keeping this external should speed things up
    print(" ")
    print(a)
    print(" ")
    #0 to 1112 and row to 
    #joint probability should look like a half triangle for the data
    #row index starts from 0 and column starts from 1. column increases by 1 each time row increases by 1. cuts computation time in half
    for r in range(0,1112):#1112
        print("Row " + str(r))
        for c in range(r+1,1111): #1111. Column 1 is the row names
            if(a==0): #Empirical
                #Average for loop comparison fan vs average set comparison enjoyer
                dfjpEmp.iat[ r,c ] = len( ALSNonZero[r]  & ALSNonZero[c]   ) / l #ALS
                dfjpCEmp.iat[ r,c ] = len(   CtrNonZero[r] & CtrNonZero[c]   ) / l #Control
            elif(a==1): #Expected ALS
                #This NEEDS to be changed to * in condensed code. this is a big bug for this. It is fixed here
                x = df.iat[r,-2]*df.iat[c,-2] #scan Emp control
                dfjpExp.iat[r,c] = x
            else: #Expected Control
                x = df.iat[r,-1]*df.iat[c,-1]
                dfjpCExp.iat[ r,c ] = x
print("Joint Frequencies Computed")
print("Saving")
dfjpEmp.set_index('ALS Empirical jf',inplace=True,drop=True)
dfjpExp.set_index('ALS Expected jf',inplace=True,drop=True)
dfjpCEmp.set_index('Ctr Empirical jf',inplace=True,drop=True)
dfjpCExp.set_index('Ctr Expected jf',inplace=True,drop=True)
dfjpEmp.to_csv(r"C:\Users\13144\Desktop\Data Analysis\Variant Analysis\Joint Probability\WGS_VariantAnalysis_JP_ALS_Emp.csv")
dfjpExp.to_csv(r"C:\Users\13144\Desktop\Data Analysis\Variant Analysis\Joint Probability\WGS_VariantAnalysis_JP_ALS_Exp.csv")
dfjpCEmp.to_csv(r"C:\Users\13144\Desktop\Data Analysis\Variant Analysis\Joint Probability\WGS_VariantAnalysis_JP_ALS_CEmp.csv")
dfjpCExp.to_csv(r"C:\Users\13144\Desktop\Data Analysis\Variant Analysis\Joint Probability\WGS_VariantAnalysis_JP_ALS_CExp.csv")
print("Saved")