import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
Ex = pd.read_csv(r"C:\Users\13144\Desktop\Data Analysis\Gene Analysis\Probability\WGS_GeneAnalyzed_Aemp.csv")
Em = pd.read_csv(r"C:\Users\13144\Desktop\Data Analysis\Gene Analysis\Probability\WGS_GeneAnalyzed_Aexp.csv")
cEx = pd.read_csv(r"C:\Users\13144\Desktop\Data Analysis\Gene Analysis\Probability\WGS_GeneAnalyzed_Cemp.csv")
cEm = pd.read_csv(r"C:\Users\13144\Desktop\Data Analysis\Gene Analysis\Probability\WGS_GeneAnalyzed_Cexp.csv")

#So basically what I'm doing first is finding the set of coordinate to be removed, the coordinates for ALS Expected and ctr Expected
#That need to be set to one so I don't divide 0/0, but instead 0/1, and then calculate fold change


#This is copied so I can find the values in the arrays for fold change, using Exp,  Emp, nExp and nEmp
#If they weren't copied I'd have to reopen the file under different variables
Exp = Ex.copy()
Emp = Em.copy()
cExp = cEx.copy()
cEmp = cEm.copy()
print("Loaded")
#converts data frame into set of nonzero or zero coordinates, depending if it is 1 or 0
def crdCreator(data,num):
    #convert to array, remove index column
    data = data.to_numpy()
    data[:,0] = 0
    #find zeroes or non zeroes, depending if it is a nonzero or zero array
    #Then creates an array of the zero and nonzero coordinates
    if(num==0):
        data = np.transpose(np.where(data==0))
    else:
        data = np.transpose(np.nonzero(data))
    return data
def toSet(data):
    #convert numpy array to set of coordinates, return set
    #if this code was put in crdCreator, it would cause an error.
    data = data.tolist()
    data = [tuple(x) for x in data]
    return set(data)
#First need to convert to numpy array, then to a set since it creates an error. I don't get the problem, but this works
Exp_zero = crdCreator(Exp,0)
Exp = crdCreator(Exp,1)
Exp = toSet(Exp)
Exp_zero = toSet(Exp_zero)
Emp_zero = crdCreator(Emp,0)
Emp = crdCreator(Emp,1)
Emp = toSet(Emp)
Emp_zero = toSet(Emp_zero)
print("ALS sets created")
cExp_zero = crdCreator(cExp,0)
cExp = crdCreator(cExp,1)
cExp = toSet(cExp)
cExp_zero = toSet(cExp_zero)
cEmp_zero = crdCreator(cEmp,0)
cEmp = crdCreator(cEmp,1)
cEmp = toSet(cEmp)
cEmp_zero = toSet(cEmp_zero)
print("Control sets created")



print("Finding coordinates to remove, and coordinates to set expected to 1")
#create set of all possible coordinate points
allCrds = set.union(Exp,Exp_zero)
#create set of common Empirical zero points (used for empirical plot)
allEmpZero = cEmp_zero & Emp_zero
#find common zeroes in all, remove from list of zeroes
allZero = Emp_zero & Exp_zero & cEmp_zero & cExp_zero
Emp_zero = Emp_zero - allZero
Exp_zero = Exp_zero - allZero
cEmp_zero = cEmp_zero - allZero
cExp_zero = cExp_zero - allZero
#create copy of E
#find common zeroes for ALS and non ALS specifically
cALS = Emp_zero & Exp_zero
cCtr = cEmp_zero & cExp_zero
#print where the numerator is not 0 and the denominator is
print("All non 0 numerator coords ALS")
print(len(Exp_zero-cALS))
print("All non 0 numerator coords control")
print(len(cExp_zero-cCtr))
#find where only Exp is 0 for ALS & non ALS, combine them
expZero = set.union(Exp_zero-cALS,cExp_zero-cCtr)
#create set for all coords to be removed
crdRemove = set.union(allZero, expZero)
#find coordinates not removed
crds = allCrds -crdRemove
print("Computed")



#needs to be set to 1 since 0/0 doesn't work, but 0/1 is 0
print("Setting certain coordinates to 1")
for crd in cALS:
    Ex.iat[ crd[0],crd[1] ] = 1
for crd in cCtr:
    cEx.iat[ crd[0],crd[1] ] = 1
print("Computed")
print("Calculating Fold Change")
listALS = []
listCtr = []
highALSCrds = []
highCtrCrds = []
for c in crds:
    a = float(Em.iat[ c[0], c[1] ]) / float(Ex.iat[ c[0],c[1] ])
    b = cEm.iat[ c[0],c[1] ] / cEx.iat[ c[0],c[1] ]
    listALS.append(a)
    listCtr.append(b)
    if a > 4:
        highALSCrds.append(c)
    elif b > 4:
        highCtrCrds.append(c)
print("Computed")







#Now the scatterplot needs to be created using the fold change for ALS in y and fold change for Ctr in x
plt.figure(figsize=(15,15))
plt.scatter(listCtr,listALS)
plt.title("Fold Change ALS vs Fold Change Ctr")
plt.xlabel("Fold Change Control")
plt.ylabel("Fold Change ALS")
plt.savefig(r"C:\Users\13144\Desktop\Data Analysis\Gene Analysis\Scatterplots\FoldChange_Scatterplot.png")
#delete scatterplot
plt.clf()
print("Saved")
print("Creating Empirical Scatterplot")

#remove common coords from ALS Expected and ALS Empirical that are 0 in both (Saves ALOT of time creating list),
#then create list where there is only 1 "0,0" coordinate

crdsEmp = allCrds ^ allEmpZero
#create value for empirical and non empirical list
listEmpALS = []
listEmpCtr = []
for c in crdsEmp:
    listEmpALS.append(Em.iat[ c[0],c[1] ])
    listEmpCtr.append(cEm.iat[ c[0],c[1] ])
#store values where ALS or control has a high fold change
print("Finding values of high fold change")
hFoldALS_ALS = []
hFoldALS_Ctr = []
hFoldCtr_Ctr = []
hFoldCtr_ALS = []
#check if index in fold change is 
for c in highALSCrds:
    hFoldALS_ALS.append(Em.iat[ c[0],c[1] ])
    hFoldALS_Ctr.append(cEm.iat[ c[0],c[1] ])
for c in highCtrCrds:
    hFoldCtr_ALS.append(Em.iat[ c[0],c[1] ])
    hFoldCtr_Ctr.append(cEm.iat[ c[0],c[1] ])
print("Computed")
print(hFoldALS_ALS[:100])
print("Creating Empirical Graph")
plt.scatter(listEmpCtr,listEmpALS)
plt.title("Empirical ALS vs Empirical Control")
plt.xlabel("Empirical Control")
plt.ylabel("Empirical ALS")
#overlay graph with points where there is high fold change, add a straight line
plt.scatter(hFoldALS_Ctr,hFoldALS_ALS,color = "orange")
plt.scatter(hFoldCtr_Ctr,hFoldCtr_ALS,color = "purple")
c = [0,.5]
plt.plot(c,c,color="black")
plt.savefig(r"C:\Users\13144\Desktop\Data Analysis\Gene Analysis\Scatterplots\Empirical_Scatterplot.png")
print("Saved")
