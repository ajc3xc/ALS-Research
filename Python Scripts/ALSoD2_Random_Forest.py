import numpy as np
from sklearn.model_selection import train_test_split
from scipy.io import arff
import pandas as pd

df = load_csv() # fill out later
list(df)
df = df.apply(lambda x: x.astype(str).str.lower())