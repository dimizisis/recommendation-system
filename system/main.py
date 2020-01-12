
import pandas as pd
import os
from infrastructure.user import User
from recommendation_system import RecommendationSystem

CURR_PATH = os.path.dirname(os.path.realpath(__file__)) + '\\'
INPUT_FILENAME = 'BX-Whole.csv'

def get_random_user(df):
    '''
    Selects a random user-id from dataframe,
    creates & returns an object of type User
    '''
    r = df.sample(1)    # take one user (randomly)
    uid=int(r['User-ID'])   # User-ID
    location=str(r['Location'].values)  # location
    age=int(r['Age'].values) if not r['Age'].isnull().values.any() else None    # handle possible NaN value to 'Age' column
    rated_books = df.loc[df['User-ID'] == uid]['ISBN'].tolist() # find all the books that are rated by the user & return them as list
    profile = df.loc[df['User-ID'] == uid].nlargest(3, ['Book-Rating'])[['ISBN', 'Book-Rating', 'Book-Title', 'Keywords', 'Book-Author', 'Year-Of-Publication']]    # user's profile is basically
                                                                                                                                                                    # the needed info to count similarity
    return User(uid, location, profile, rated_books, age)

if __name__ == '__main__':  
    df = pd.read_csv(CURR_PATH + INPUT_FILENAME, encoding='unicode_escape', sep=';')
    rec_system = RecommendationSystem(df)   # create a recommendation system
    user1 = get_random_user(df)
    recommended_books_jacc = rec_system.get_recommended_books(user1)   # get the recommended books for the random user (jaccard by default for keyword list similarity)
    recommended_books_dice = rec_system.get_recommended_books(user1, keyword_similarity_method='dice')   # get the recommended books for the random user (jaccard by default for keyword list similarity)

    print('============= Jaccard =============')
    print(recommended_books_jacc)

    print('============= Dice =============')
    print(recommended_books_dice)
