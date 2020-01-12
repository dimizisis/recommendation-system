
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
    r = df.sample(1)
    uid=int(r['User-ID'])
    location=str(r['Location'].values)
    age=int(r['Age'].values) if not r['Age'].isnull().values.any() else None
    rated_books = df.loc[df['User-ID'] == uid]['ISBN'].tolist()
    profile = df.loc[df['User-ID'] == uid].nlargest(3, ['Book-Rating'])[['ISBN', 'Book-Rating', 'Book-Title', 'Keywords', 'Book-Author', 'Year-Of-Publication']]
    return User(uid, location, profile, rated_books, age)

if __name__ == '__main__':  
    df = pd.read_csv(CURR_PATH + INPUT_FILENAME, encoding='unicode_escape', sep=';')
    rec_system = RecommendationSystem(df)
    recommended_books = rec_system.get_recommended_books(get_random_user(df))
