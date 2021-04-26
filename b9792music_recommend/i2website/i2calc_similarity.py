import os
import csv
from termcolor import colored
import pandas as pd
import i0read_csv

if __name__ == "__main__":
    ratings = pd.read_csv('music_rating.csv')
    print(ratings)
    pivot_ratings = ratings.pivot_table(columns='critic',
                                        index='title',
                                        values='rating')
    print(pivot_ratings.to_string())

    print(colored('相似度计算=======>', 'red', attrs=['reverse', 'blink']))
    print('Claudia Puig', pivot_ratings['Claudia Puig'])
    cor_pr = pivot_ratings.corrwith(pivot_ratings['Claudia Puig'])
    print(cor_pr,'\n')

    sm = pivot_ratings.corr()
    print(sm.to_string())
    print(colored('可以看出: Lisa Rose ~Toby with 0.99 和 Mick LaSalle ~ Toby 0.92', 'red'))