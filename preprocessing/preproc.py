
import pandas as pd
import os
import nltk
# nltk.download('stopwords')
# nltk.download('punkt')

CURR_PATH = os.path.dirname(os.path.realpath(__file__)) + '\\'
BOOK_RATINGS_FILENAME = 'BX-Book-Ratings.csv'
BOOK_USERS_FILENAME = 'BX-Users.csv'
BOOKS_FILENAME = 'BX-Books.csv'
OUTPUT_FILENAME = 'BX-Whole.csv'

def read_csv_files():
    '''
    Reading all CSV files (must be in the same folder with .py file)
    '''
    try:
        print('Reading files...')
        ratings_df = pd.read_csv(CURR_PATH + BOOK_RATINGS_FILENAME, encoding='unicode_escape', sep=';')
        users_df = pd.read_csv(CURR_PATH + BOOK_USERS_FILENAME, encoding='unicode_escape', sep=';', escapechar='\\')

        book_fields = ['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher'] # read only these fields from csv (removed URLs)
        books_df = pd.read_csv(CURR_PATH + BOOKS_FILENAME, encoding='unicode_escape', sep=';', escapechar='\\', usecols=book_fields)
        print('Files read.')
    except Exception as e:
        print(e)
        exit(-1)

    return ratings_df, users_df, books_df

def create_keywords(sentence):
    '''
    Given a sentence, returns a keywords list
    after being preprocessed (punctuation removal, tokenize, stopwords removal, stemming)
    '''
    sentence = remove_punctuation(str.lower(sentence))
    word_tokens = tokenize(sentence)
    word_tokens = remove_stopwords(word_tokens)
    keywords = stem(word_tokens)
    return keywords

def remove_punctuation(sentence):
    '''
    Given a sentence (string), returns the sentence without
    punctuation (string)
    '''
    import string
    return sentence.translate(str.maketrans('', '', string.punctuation))

def tokenize(sentence):
    '''
    Given a sentence (string), returns the word tokens (list)
    '''
    from nltk.tokenize import word_tokenize
    return word_tokenize(sentence)

def remove_stopwords(word_tokens):
    '''
    Given word tokens (list of strings), removes stopwords
    Only English lowercase stopwords are supported
    Returns filtered sentence (list)
    '''
    from nltk.corpus import stopwords 
    stop_words = set(stopwords.words('english'))  
    filtered_sentence = [] 
    for w in word_tokens: 
        if w not in stop_words: 
            filtered_sentence.append(w) 
    return filtered_sentence

def stem(word_tokens, method='porter'):
    '''
    Given word tokens (list of strings), performs stemming.
    Default stem method is porter, snowball's method
    is also supported
    Returns stemmed tokens (list)
    '''
    if method == 'porter':
        from nltk.stem import PorterStemmer
        s = PorterStemmer() 
    elif method == 'snowball':
        from nltk.stem import SnowballStemmer
        s = SnowballStemmer('english')
    stemmed_tokens = []
    for w in word_tokens: 
        stemmed_tokens.append(s.stem(w))
    return stemmed_tokens

def create_df(book_ratings_df, users_df, books_df):
    '''
    Creating a big pandas dataframe, with all the info
    we need. The dataframe return will be used for preprocessing
    Returns joinned dataframe
    '''
    dataframe = book_ratings_df.join(users_df.set_index('User-ID'), on='User-ID', how='left')
    dataframe = dataframe.join(books_df.set_index('ISBN'), on='ISBN', how='left')
    return dataframe

def preprocess(dataframe):
    '''
    Preprocessing according to the instructions, given
    a pandas dataframe
    Returns preprocessed dataframe
    '''
    print('Preprocessing dataframe...')
    dataframe = dataframe.groupby('ISBN').filter(lambda x : len(x)>9)   # delete all rows with books that have less than 9 reviews
    dataframe = dataframe.groupby('User-ID').filter(lambda x : len(x)>4)    # delete all users that reviewed less than 4 books
    keywords = []
    for title in dataframe['Book-Title']:
        try:
            str.lower(title)
        except:
            title = ''
        keywords.append(create_keywords(title))
    dataframe['Keywords'] = keywords
    print('Preprocessing OK.')

    dataframe = dataframe[dataframe['Book-Title'] != '']    # drop rows with empty values in title
    
    return dataframe.dropna(subset=['Book-Title']) # drop rows with nan values in title

def export_to_csv(dataframe, outfilename):
    '''
    Export a pandas dataframe to csv with specific filename
    '''
    try:
        dataframe.to_csv(CURR_PATH + outfilename, encoding='utf-8', sep=';', index=False)  # export to csv
        print('CSV exported.')
    except Exception as e:
        print(e)
        exit(-1)

book_ratings_df, users_df, books_df = read_csv_files()
df = create_df(book_ratings_df, users_df, books_df)
df = preprocess(df)
export_to_csv(df, OUTPUT_FILENAME)
