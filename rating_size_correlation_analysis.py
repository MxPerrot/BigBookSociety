# -*- coding: utf-8 -*-

"""
IUT de Lannion
BUT Informatique 3
SAE 5.C.01

Wizards of the West Coast

Maxime Perrot 3C2

Created on 2024-10-08
"""

#######################################
#               IMPORTS               #
#######################################

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

#######################################
#              CONSTANTS              #
#######################################

CSV_FILE = 'data/Cleaned_books.csv'


#######################################
#                 MAIN                #
#######################################

def main():
    data = pd.read_csv(CSV_FILE)

    df = data[
        [
        "average_rating",
        "number_of_pages"
        ]
    ]

    df = df[df["number_of_pages"] > 0] # Remove books with 0 pages
    df = df[df["number_of_pages"] < 2000]

    df = df.sort_values('average_rating')

    x = df['number_of_pages'].to_numpy()
    y = df['average_rating'].to_numpy()

#    xy = np.vstack([x,y])
#    z = gaussian_kde(xy)(xy)

    ymin = [min(y[:i]) for i in range(1,len(x)+1)]


    plt.scatter(x,y,s=1)
    plt.plot(x,ymin)
    plt.xlabel('Number of pages')
    plt.ylabel('Average rating')
    plt.show()


if __name__ == "__main__":
    main()
