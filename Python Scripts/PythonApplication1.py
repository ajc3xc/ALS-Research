import numpy as np
import matplotlib.pyplot as plt

arr = np.loadtxt(r"C:\Users\13144\Downloads\DataForProblem1.txt", dtype = int)
#print(arr)

print("Adam Camerer")
print("")
print("Q1 answers")
print("")
print("(a) mean and std")
print(np.mean(arr))
print(np.std(arr))
print("")





print("(b) 1st and 3rd quartiles")
p75, p25 = np.percentile(arr, [75, 25])
print(p25)
print(p75)
print("")





print("(c) outliers")

print("Are max and min outliers?")
median = np.median(arr)
iqr = p75 - p25
lower = p25 -1.5 * (p75 - p25)
upper = p75 + 1.5 * (p75 - p25)
print(str(lower) + " " + str(upper))
Max = np.max(arr)
Min = np.min(arr)
print(Max > upper)
print(Min < lower)
print("Are there any outliers that are not the max or min?")
print("False")
print("")






print("(e) IQR")
print(iqr)
print("")





print("(f) observations not in 1 std deviation")
mean = np.mean(arr)
std = np.std(arr)
StdOutliers = len(np.where(arr > (mean + std))) + len(np.where(arr < (mean - std)))
print(len(arr) - StdOutliers)






#d

plt.boxplot(arr)
plt.title("Adam Camerer Company values") 
plt.show()
plt.savefig(r"C:\Users\13144\Desktop\Stat 3115\Quiz1\Q1_Answers(d)")