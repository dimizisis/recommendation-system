
# Content-Based Recommendation System

## Description
A content-based recommendation system for books (see dataset below). The program chooses a random user & takes his best 3 ratings. Based on these 3 ratings, recommends to the user 10 books, which may like. The recommended books are based on 3 factors:

1. Books' titles Keyword similarity (Jaccard Similarity or Dice Coefficient)
2. Book author equality
3. Publish Year Difference

## Instructions
```
pip install -r requirements.txt
```
### Preprocessing

The 3 initial CSV files must be in the same folder with preproc.py. When you run the file for the first time, please uncomment the lines 5 and 6:

```
# nltk.download('stopwords')
# nltk.download('punkt')
```

### Recommendation System

The BX-Whole CSV file must be in the same folder with main.py

## Preprocessing

From the initial dataset, we remove:

1. The books that have less than 10 ratings
2. Users that have rated less than 5 books

After the removals mentioned, we create keywords for each book title, based on the title. Specifically, to generate keywords, we perform to each book title:

1. Tokenization
2. Stop word removal
3. Stemming (by default with Porter's algorithm, snowball's also supported)

Every book now has a keywords list, which is attached to dataframe (new column).

At the end, we join all tables (BX-Books, BX-Book-Ratings, BX-Users) into a new dataframe that contains all the information needed.

We create the BX-Whole.csv file, which is going to be the input for our recommendation system.

## Usage

### Preprocessing

```
python preproc.py
```
### Recommendation System

```
python main.py
```

## Dataset

[Book-Crossing dataset](http://www2.informatik.uni-freiburg.de/~cziegler/BX/ "Link to Dataset")
