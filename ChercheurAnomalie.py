import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv("data/books.csv")

#cols = ["Unnamed: " + str(i) for i in range(24,86)]
str_column="Unnamed: "

#print(data.shape)

#Purge des lignes contenant des informations dans des colonnes inexistantes

for i in range(24,87):
    index = 0
    for y in data[str_column+str(i)]:
        if (pd.notna(y)):
            data = data.drop([index])
        index += 1
            
#Purge des colonnes inexistantes

for i in range(24,87):
 data = data.drop(columns=[str_column+str(i)])

print(data.columns)
print(data.shape)

