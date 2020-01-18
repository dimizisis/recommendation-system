
import json
import os
import sys
from pprint import pprint
from operator import itemgetter

CURR_PATH = os.path.dirname(os.path.realpath(__file__)) + '\\'

def open_files():
    '''
    Opens files (in the same directory)
    Filenames are entered by user as arguments
    Returns the files' data
    '''
    try:
        filenames = [sys.argv[1], sys.argv[2]]
    except:
        print('Usage: <filename1> <filename2>')
        exit(-1)
    file_data = list()
    for f_name in filenames:
        with open(CURR_PATH+f_name) as f:
            file_data.append(json.load(f))

    return file_data

def create_list(file_data):
    '''
    Creates final recommendations list
    Returns the list
    '''
    books_isbn = list() # we need this list to find the frequency of books
    for rec_books in file_data:
        for book in rec_books:
            books_isbn.append(book['ISBN'])
    
    recommendations_list = list()   # the final recommendations list
    for rec_books in file_data:
        for book in rec_books:
            book['count'] = books_isbn.count(book['ISBN'])
            recommendations_list.append(book)

    return recommendations_list

file_data = open_files()

recommendations_list = create_list(file_data)

recommendations_list = sorted(recommendations_list, key=itemgetter('count', 'similarity'), reverse=True)    # primary key to sort: count, secondary: similarity

pprint(recommendations_list)
