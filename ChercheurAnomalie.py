import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv("data/books.csv")

#cols = ["Unnamed: " + str(i) for i in range(24,86)]
str_column="Unnamed: "

#print(data.shape)

#Purge des lignes contenant des informations dans des colonnes inexistantes

for i in range(24,86):
    index = 0
    for y in data[str_column+str(i)]:
        # remove rows 
        if (pd.notna(y)):
            data = data.drop([index])
        index += 1
            
print(data.columns)

data = data.drop(data["Unnamed: 24"], axis=1)

#Purge des colonnes inexistantes

for i in range(24,86):
#    data = data.drop(columns=data[str_column+str(i)])


