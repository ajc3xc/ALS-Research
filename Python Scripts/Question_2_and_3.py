import numpy as np
import matplotlib.pyplot as plt

#Question 2
arr = np.empty(2000, dtype = int)
for x in range(2000):
    if x <1302: arr[x] = 1
    else: arr[x] = 0

plt.hist(arr)
plt.title("Adam Camerer Question 2")
plt.savefig(r"C:\Users\13144\Desktop\Stat 3115\Quiz1\Q2_answers(e)")
plt.show()