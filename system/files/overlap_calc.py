
import json
import os
import sys

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

def calc_avg_overlap(list1, list2):
    '''
    Calculate average overlap between 2 lists
    Returns the avg overlap (float)
    '''
    summation=0
    set1 = set()
    set2 = set()
    for i in range(len(list1)):
        set1.add(list1[i])
        set2.add(list2[i])
        summation += len(set1.intersection(set2))

    return summation/len(list1)

file_data = open_files()

avg_overlap = calc_avg_overlap(list1=[recommendation['ISBN'] for recommendation in file_data[0]], list2=[recommendation['ISBN'] for recommendation in file_data[1]])

print(f'Average overlap: {avg_overlap}')
