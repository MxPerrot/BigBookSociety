import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv("data/books.csv")

str_column="Unnamed: "

for i in range(24,86):
    for y in data[str_column+str(i)]:
        if (y != ):
            print(y)