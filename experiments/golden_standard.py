
import json
import os
import sys
import re
from pprint import pprint
from operator import itemgetter

FILES_PATH = os.path.dirname(os.path.realpath(__file__)) + '\\files\\'

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
        with open(FILES_PATH+f_name) as f:
            file_data.append(json.load(f))

    return file_data, re.findall("\d+", filenames[0])[0]

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
            if book_already_exists(recommendations_list, book): # if there is the specific ISBN in rec list (if we added it in previou iteration)
                if has_greater_similarity(recommendations_list, book):  # if the book (with the same ISBN) has greater similarity than the one in list (the same books with different similarities)
                    replace(recommendations_list, book)
            else:      
                book['count'] = books_isbn.count(book['ISBN'])
                recommendations_list.append(book)

    return recommendations_list

def replace(lst, book):
    '''
    Replaces similarity if needed
    Takes as parameters a list and a book (dict)
    book has the similarity that need to be replaced
    '''
    for b in lst:
        if b['ISBN'] == book['ISBN']:
            b['similarity'] = book['similarity']
            return

def has_greater_similarity(lst, book):
    '''
    Checks if the book (dict, with the same ISBN) 
    has greater similarity than the one in list (the same books with different similarities)
    Returns True if it has, False if it doesn't
    '''
    for b in lst:
        if book['ISBN'] == b['ISBN']:
            if book['similarity'] > b['similarity']:
                return True
            return False
    return True

def book_already_exists(lst, book):
    '''
    Checks if a book's ISBN is already in list
    Takes the book (dict) and a list (of dicts) as parameters
    Returns True if exists, False if not
    '''
    for b in lst:
        if book['ISBN'] == b['ISBN']:
            return True
    return False

def write_golden_standard_to_file(user_id, recommendations):
    with open(f'{FILES_PATH}{uid}-golden-standard.json', 'w') as file:
        file.write(json.dumps(recommendations, indent=4))
        print('\nfile written')

file_data, uid = open_files()    # open the files (the name of the files given as parameters)

recommendations_list = create_list(file_data)   # create the list of books (golden standard)

recommendations_list = sorted(recommendations_list, key=itemgetter('count', 'similarity'), reverse=True)    # primary key to sort: count, secondary: similarity

pprint(recommendations_list)

write_golden_standard_to_file(uid, recommendations_list)
