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
#                 MAIN                #
#######################################

def main(data, show_graphs=False):

    df = data[
        [
        "rating_count",
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

    # Number of components to keep
    eig = pd.DataFrame({
        "Dimension" : range(1,len(df_scaled.columns) + 1),
        "Eigenvalue" : pca.explained_variance_,
        "Eigenvalue (%)": pca.explained_variance_ratio_*100,
        "Cumulative (%)": np.round(np.cumsum(pca.explained_variance_ratio_)*100)
    })

    # Plot the eigenvalues
    plt.bar(eig["Dimension"], eig["Eigenvalue (%)"], color = "blue")
    plt.plot(eig["Dimension"], eig["Cumulative (%)"], color = "red", marker = "o")
    plt.xlabel("Dimensions")
    plt.ylabel("Eigenvalues (%)")
    plt.title("PCA Explained Variance")
    plt.legend(["Cumulative (%)", "Eigenvalue (%)"])
    plt.xticks(ticks=range(1, len(eig["Dimension"]) + 1), labels=range(1, len(eig["Dimension"]) + 1))
    plt.savefig("./graphs/BarChart_PCA_Explained_Variance.png", bbox_inches="tight")
    if show_graphs: plt.show()
    plt.clf()
    
    # Plot the biplot
    biplot(
        score = df_pca[:,0:2],
        coeff = np.transpose(
            pca.components_[0:2,:]
        ),
        cat          = pca.explained_variance_ratio_[0:1],
        density      = True,
        coeff_labels = list(df.columns),
        title        = 'Correlation circle of the rating count,\naverage rating and number of pages of the books',
        show_graph   = show_graphs,
        save_path    = "./graphs/Biplot_PCA_Correlation_Circle.png"
    )

if __name__ == "__main__":

    CSV_FILE = 'data/Cleaned_books.csv'

    data = pd.read_csv(CSV_FILE)
    main(data=data, show_graphs=False)

