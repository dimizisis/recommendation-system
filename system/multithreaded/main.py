
import pandas as pd
import os
from infrastructure.user import User
from recommendation_system import RecommendationSystem
from queue import Queue
import threading

CURR_PATH = os.path.dirname(os.path.realpath(__file__)) + '\\'
INPUT_FILENAME = 'BX-Whole.csv'
NUM_USERS = 5

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

def write_recommendations_to_file(q_element):
    '''
    Writes recommendation to file (for a user and specific method)
    Takes a dictionary as parameter (from queue)
    '''
    import json
    uid = q_element['uid']
    method = q_element['method']
    recs = q_element['recommendations']
    with open(f'{CURR_PATH}{uid}-{method}.json', 'w') as file:
        file.write(json.dumps(recs, indent=4))
        print('file written')

def create_user_lst(df):
    '''
    Creates the users list
    Takes the dataframe as parameter (created by BX-Whole.csv)
    Returns the user list
    '''
    user_lst = list()
    for i in range(NUM_USERS):
        user_lst.append(get_random_user(df))

    return user_lst

def create_thread_lst(rec_system, users):
    '''
    Creates the thread list with length (NUM_USERS x 2)
    Takes the recommendation system object and the user list as parameters
    Returns the thread list
    '''
    thread_lst = list()
    for i in range(NUM_USERS):
        thread_lst.append(threading.Thread(None, target=rec_system.get_recommended_books, args=(q, users[i],)))

    for i in range(NUM_USERS):
        thread_lst.append(threading.Thread(None, target=rec_system.get_recommended_books, args=(q, users[i], 'dice',)))

    return thread_lst

def start_threads_and_wait(threads):
    '''
    Starts all threads
    and blocks until all threads are finished
    Takes the thread list as parameter
    '''
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

def write_files(q):
    '''
    Calls the write recommendations to file function
    for each element in queue
    Takes the thread list as parameter
    '''
    for element in list(q.queue):
        write_recommendations_to_file(element)

if __name__ == '__main__':  
    df = pd.read_csv(CURR_PATH + INPUT_FILENAME, encoding='unicode_escape', sep=';')
    rec_system = RecommendationSystem(df)   # create a recommendation system

    q = Queue()    # the queue we will use for threads

    user_lst = create_user_lst(df)  # generate random <NUM_USERS> users

    thread_lst = create_thread_lst(rec_system, user_lst)    # create the thread list (with length NUM_USERS x 2)

    start_threads_and_wait(thread_lst)  # start threads and wait until every thread is finished

    write_files(q)  # write all recommendations to separate files (num of files: NUM_USERS x 2)
