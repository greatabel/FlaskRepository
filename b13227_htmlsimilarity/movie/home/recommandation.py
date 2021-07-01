import os
import csv

import pandas as pd


def recommend(demo, ratings, pivot_ratings):

    missing_films = list(pivot_ratings[pivot_ratings[demo].isnull()].index)
    print(missing_films)


    mean_score = pivot_ratings[demo].mean()
    print('mean_score=', mean_score)

    remain_films = ratings[ratings['title'].isin(missing_films)]
    remain_films.is_copy = False
    remain_films['similarity'] = remain_films['critic'].map(sm[demo].get)
    remain_films['sim_rating'] = remain_films.similarity * remain_films.rating

    print(remain_films)

    rec = remain_films.groupby('title').apply(lambda s: s.sim_rating.sum() / s.similarity.sum())

    print(rec)
    rec = rec[rec >= mean_score]
    print('该用户我推荐：', list(rec.index))


def main():
    print('main')
    data_path = os.path.join('movie', 'home')
    mypath = os.path.join(data_path, 'movie_rating.csv')
    print(mypath)
    ratings = pd.read_csv(mypath)
    
    pivot_ratings = ratings.pivot_table(columns='critic',
                                        index='title',
                                        values='rating')

    print(pivot_ratings.to_string())
    
    sm = pivot_ratings.corr()
    print(sm.to_string())

    demo = 'Toby'
    # print(colored('1. 找出该用户为打分的电影 =>', 'red', attrs=['reverse', 'blink']))
    missing_films = list(pivot_ratings[pivot_ratings[demo].isnull()].index)
    print(missing_films)
    # print(colored('2. 找出该用户已打分的平均分=>', 'red', attrs=['reverse', 'blink']))

    mean_score = pivot_ratings[demo].mean()
    print(mean_score)
    # print(colored('3. 处理原始表，加上相似性列，筛选出未打分 =>', 
    #               'red', attrs=['reverse', 'blink']))
    remain_films = ratings[ratings['title'].isin(missing_films)]
    remain_films.is_copy = False
    remain_films['similarity'] = remain_films['critic'].map(sm[demo].get)
    remain_films['sim_rating'] = remain_films.similarity * remain_films.rating

    print(remain_films)
    # print(colored('4. 汇总算出电影平均相似值 =>', 
    #               'red', attrs=['reverse', 'blink']))
    rec = remain_films.groupby('title').apply(lambda s: s.sim_rating.sum() / s.similarity.sum())

    print(rec)
    rec = rec[rec >= mean_score]
    print('该用户我推荐：', list(rec.index))
    return  list(rec.index)