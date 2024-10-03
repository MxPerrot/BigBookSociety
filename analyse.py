import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv("data/Cleaned_authors.csv")

dico={
}

for index, row in data.iterrows():
    for i in row['author_genres'].split(','):
        if(i not in dico):
            dico[i] = [['Male',0],['Female',0]]
        if row['author_gender']=='male':
            dico[i][0][1] = dico[i][0][1]+1
        else:
            dico[i][1][1] = dico[i][1][1]+1

for i in dico:
    print(i,dico[i])