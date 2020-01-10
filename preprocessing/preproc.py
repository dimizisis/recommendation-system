
import pandas as pd
import os

CURR_PATH = os.path.dirname(os.path.realpath(__file__)) + '\\'
BOOK_RATINGS_FILENAME = 'BX-Book-Ratings.csv'
BOOK_USERS_FILENAME = 'BX-Users.csv'
BOOKS_FILENAME = 'BX-Books.csv'
OUTPUT_FILENAME = 'BX-Whole.csv'

def read_csv_files():
    '''
    Reading all CSV files (must be in the same folder with .py file)
    '''
    return pd.read_csv(CURR_PATH + BOOK_RATINGS_FILENAME, encoding='unicode_escape', sep=';'), pd.read_csv(CURR_PATH + BOOK_USERS_FILENAME, encoding='unicode_escape', sep=';', escapechar='\\'), pd.read_csv(CURR_PATH + BOOKS_FILENAME, encoding='unicode_escape', sep=';', escapechar='\\')

def create_df(book_ratings_df, users_df, books_df):
    '''
    Creating a big pandas dataframe, with all the info
    we need. The dataframe return will be used for preprocessing
    '''
    dataframe = book_ratings_df.join(users_df.set_index('User-ID'), on='User-ID', how='left')
    dataframe = dataframe.join(books_df.set_index('ISBN'), on='ISBN', how='left')
    return dataframe

def preprocess(dataframe):
    '''
    Preprocessing according to the instructions, given
    a pandas dataframe
    '''
    dataframe = dataframe.groupby('ISBN').filter(lambda x : len(x)>9)   # delete all rows with books that have less than 9 reviews
    dataframe = dataframe.groupby('User-ID').filter(lambda x : len(x)>4)    # delete all users that reviewed less than 4 books
    return dataframe

book_ratings_df, users_df, books_df = read_csv_files()

df = create_df(book_ratings_df, users_df, books_df)

df = preprocess(df)

df.to_csv(CURR_PATH + OUTPUT_FILENAME, encoding='utf-8', sep=';', index=False)  # export to csv
