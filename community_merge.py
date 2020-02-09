# -*- coding: utf-8 -*-

import os
import pandas as pd


def same_category_save(df, text, save_file_name, base_dir):
    print(text, len(df))

    df = df[['date_created', 'title', 'content']]
    df = df[(df.content.str.contains(text) == True) | (df.title.str.contains(text) == True)]
    df.drop(['title'], axis=1, inplace=True)

    df.sort_values(by=['date_created'], ascending=[False], inplace=True)
    df.to_csv(os.path.join(base_dir, save_file_name), mode='w', index=False, encoding='utf-8')
    
    print(text, len(df))
    

if __name__ == '__main__':
    file_list = os.listdir('data_c/')
    file_list.sort()

    dfs = {}
    for f in file_list:
        if 'daum_2019' in f or 'naver_2019' in f:
            # file_name: daum_년도_post_게시판아이디.csv / naver_년도_post_게시판아이디.csv
            split_name = os.path.splitext(f)[0].split('_')
            key = split_name[0] + '_' + split_name[-1]
            dfs[key] = pd.read_csv('data_c/' + f, encoding='utf-8')

    # for key, val in dfs.items():
    #     print(key)
    #     print(val.head())

    df_total = pd.concat([dfs['naver_'], dfs['daum_']])
    same_category_save(df_total, '모바일', 'total_2019.csv')
