
import pandas as pd
import matplotlib.pyplot as plt

#input list of values here
list = [87, 103, 130, 160, 180, 195, 132, 145, 211, 105, 145, 153, 152, 138, 87, 99, 93, 119, 129]
col = {"data":[int(x) for x in list]}

df = pd.DataFrame(col)

print(df.describe())
print(df.quantile(.5)) #print percentile (0-1 -> 0-100%)

#outliers automatically shown
plt.boxplot(df['data']);
plt.show();