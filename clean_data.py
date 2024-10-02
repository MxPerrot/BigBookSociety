# -*- coding:utf-8 -*-

"""
This module cleans the DataFrame generated from books.csv
"""

#######################################
#               IMPORTS               #
#######################################

import numpy as np
import pandas as pd

#######################################
#              CONSTANTS              #
#######################################

COLUMNS_TYPES = {
    "id":int,
    "title":str,
    "series":str,
    "author":str,
    "rating_count":int,
    "review_count":int,
    "average_rating":float,
    "five_star_ratings":int,
    "four_star_ratings":int,
    "three_star_ratings":int,
    "two_star_ratings":int,
    "one_star_ratings":int,
    "number_of_pages":int,
    "date_published":str,
    "publisher":str,
    "original_title":str,
    "genre_and_votes":str,
    "isbn":str,
    "isbn13":int,
    "settings":str,
    "characters":str,
    "awards":str,
    "books_in_series":str,
    "description":str,
}

BOOKS_CSV = "data/books.csv"


#######################################
#              FUNCTIONS              #
#######################################

def load_data(csv_file):
    """
    Load data from a CSV file
    """

    return pd.read_csv(csv_file, dtype=COLUMNS_TYPES)





#######################################
#                MAIN                 #
#######################################

def main():
    """
    Main function
    """

    data = load_data(BOOKS_CSV)


if __name__ == "__main__":
    main()