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
import seaborn
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from libs.biplot import biplot

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
        "rating_count",
        "review_count",
        "average_rating",
        "number_of_pages"
        ]
    ]

    df = df[df["number_of_pages"] > 0] # Remove books with 0 pages

    # Standardize the data
    temp = df.sub(df.mean())
    df_scaled = temp.div(df.std())

    # Apply PCA
    pca = PCA()
    df_pca = pca.fit_transform(df_scaled)

    # Plot the explained variance ratio
    plt.bar(range(len(pca.explained_variance_ratio_)), pca.explained_variance_ratio_)
    plt.show()

    # Plot the biplot
    biplot(
        score = df_pca[:,0:2],
        coeff = np.transpose(
            pca.components_[0:2,:]
        ),
        cat          = pca.explained_variance_ratio_[0:1],
        density      = True,
        coeff_labels = list(df.columns)
    )


if __name__ == "__main__":
    main()
