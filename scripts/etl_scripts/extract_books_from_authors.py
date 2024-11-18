# -*- coding:utf-8 -*-

"""

IUT de Lannion
BUT Informatique 3
SAE 5.C.01

Wizards of the West Coast

Maxime Perrot
Damien Goupil

Created on 2024-11-06

This module extracts the books from the authors.csv with the intention to append the extracted values to books.csv

For now this program will only detect the books that are in authors but not in books.
"""

import pandas as pd
import numpy as np

def main(chemin_fichier_livres_complet):

    """
    Main function
    """
    
    # Load authors.csv
    authors = pd.read_csv("data/Cleaned_authors.csv")

    # Load books.csv
    books = pd.read_csv("data/Cleaned_books.csv")

    # Get a list of books in the authors ("book_title" column)
    books_in_authors = authors["book_id"].unique()

    # Check for all ids in books_in_authors that are also in books["id"]
    books_in_books = books["id"].unique()

    # Get the common ids between books_in_authors and books_in_books

    common_books_id = np.intersect1d(books_in_authors, books_in_books)
    
    rows_authors_books = authors.loc[authors['book_id'].isin(common_books_id)]

    col_list = ['book_id', 'author_id']

    link_dataframe = rows_authors_books[col_list]

    link_dataframe = link_dataframe.drop_duplicates(subset = ['book_id','author_id'], keep=False)

    

    #rows_authors_books = rows_authors_books.drop_duplicates(subset=['book_id'])

    #common_books_titles_with_id = rows_authors_books.loc[rows_authors_books['book_id'].isin(common_books_id) & (rows_authors_books['book_title'].isin(rows_books_books['title']))]
    #not_common_books_titles_with_id = rows_authors_books.loc[rows_authors_books['book_id'].isin(common_books_id) & (~rows_authors_books['book_title'].isin(rows_books_books['title']))]
    # Print the number of common books
    #print(f"Number of common books by ID: {len(common_books_id)}")
    #print(f"Number of common books by ID and title: {len(common_books_titles_with_id)}")
    #print(f"Number of common books by ID but not title: {len(not_common_books_titles_with_id)}")


    #print(f"Books with matching ID but not title: {not_common_books_titles_with_id['book_id']}")
    # Conclusion 1 from analysis : All common books that have the same ID but not the same title are the same books with erronous title.


    # Filter authors.csv to keep only authors who have a book in books.csv
    #authors_with_books = authors[common_books]


    ###### Analysis of books with different IDs yet a similar TITLE
    rows_authors_books = authors.loc[authors['book_title'].isin(books['title'])]
    rows_books_books = books.loc[books['title'].isin(authors['book_title'])]

    common_books_titles_but_not_ID = rows_authors_books.loc[~rows_authors_books['book_id'].isin(common_books_id) & (rows_authors_books['book_title'].isin(rows_books_books['title']))]

    common_books_titles_but_not_ID = common_books_titles_but_not_ID[col_list]

    link_dataframe = pd.concat([link_dataframe,common_books_titles_but_not_ID])
    
    # print(f"Number of common books titles but not ID: {len(common_books_titles_but_not_ID)}")
    # print(f"Common books titles but not ID by title: {common_books_titles_but_not_ID['book_title']}")

    # Conclusion 2 from analysis : It seems common books by title yet not by ID seem to only have a problem with an Erronous ID.




    #################################  INFO FOR AFTER ANALYSIS  ###############################################################################################################################################
    # for common_books_id, free to drop fully info in authors.csv and just keep info in books.csv. Take link between authors id and books id and put them in common link DF
    # for common_books_titles_but_not_ID, free to drop info in authors.csv. Take the ID in books and remake the link in common link DF
    # for books in authors that do not have either common name or title create books directly
    #
    #
    ############################################################################################################################################################################################################


    rows_authors_books_big = authors.loc[(~authors['book_title'].isin(books['title']) & (~authors['book_id'].isin(common_books_id)))]
    # book_average_rating,book_id,book_title,genre_1,genre_2,num_ratings,num_reviews,pages,publish_date

    # TODO Search books with multiple authors and print their titles
    # g = rows_authors_books_big.groupby('book_id')['author_id'].unique()
    # g = g.where(g.str.len()>1).dropna()

    # rows_authors_books_big = rows_authors_books_big.loc[~rows_authors_books_big['book_id'].isin(g.index.tolist())]

    link_dataframe = pd.concat([link_dataframe,rows_authors_books_big[col_list]])

    rows_authors_books_big = rows_authors_books_big.drop(columns=['author_average_rating', 'num_reviews', 'num_ratings', 'author_gender','author_genres','author_id','author_rating_count','author_review_count','birthplace'])

    rows_authors_books_big = rows_authors_books_big.rename(columns={"book_id": "id","author_name": "author","book_average_rating": "average_rating","book_title": "title","pages": "number_of_pages","publish_date": "date_published"})

    bigBook = pd.concat([books,rows_authors_books_big])

    bigBook = bigBook.drop(columns=['author'])

    bigBook = bigBook.drop_duplicates()

    link_dataframe = link_dataframe.loc[link_dataframe['book_id'].isin(bigBook['id'])]

    bigBook.to_csv(chemin_fichier_livres_complet, index=False)

    bigBook.to_csv("data/complete_book_copy.csv", index=False)

    link_dataframe.to_csv("data/populate/link.csv", index=False)

    #Remaining Values
    #genre_1,genre_2,publish_date

    #Books Values
    #series,rating_count,review_count,average_rating,five_star_ratings,four_star_ratings,three_star_ratings,two_star_ratings,one_star_ratings,number_of_pages,date_published,publisher,original_title,genre_and_votes,isbn,isbn13,settings,characters,awards,books_in_series,description,description_length,title_length,series_length


    #TWO BOOKS WITH MULTIPLE AUTHORS



if __name__ == "__main__":
    main(
        chemin_fichier_livres_complet = "data/complete_book.csv"
    )
