
import pandas as pd
import os
import ast
from infrastructure.user import User

CURR_PATH = os.path.dirname(os.path.realpath(__file__)) + '\\'
INPUT_FILENAME = 'BX-Whole.csv'

class RecommendationSystem:

    def recommend(self, user):
        pass

def get_random_user(df):
    r = df.sample(1)
    uid=int(r['User-ID'])
    location=str(r['Location'].values)
    age=int(r['Age'].values) if not r['Age'].isnull().values.any() else None
    # lst = ast.literal_eval(df['Keywords'][2]) # get keywords as list
    print(df.loc[df['User-ID'] == uid].nlargest(3, ['Book-Rating']))
    return User(uid, location, age)

if __name__ == '__main__':  
    df = pd.read_csv(CURR_PATH + INPUT_FILENAME, encoding='unicode_escape', sep=';')
    user = get_random_user(df)
