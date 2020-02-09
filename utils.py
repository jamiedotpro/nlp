# -*- coding: utf-8 -*-

import os
import re
import pandas as pd
import numpy as np
from itertools import permutations, combinations
from collections import Counter
import np_func as npf
import matplotlib.pyplot as plt
import datetime

from gensim import corpora
from gensim import models
# 주제를 워드 크라우드로 시각화하기
import matplotlib.pyplot as plt
from wordcloud import WordCloud


# 유니코드 한글 시작 : 44032, 끝 : 55199
BASE_CODE, CHOSUNG, JUNGSUNG = 44032, 588, 28

# 초성 리스트. 00 ~ 18
CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

# 중성 리스트. 00 ~ 20
JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']

# 종성 리스트. 00 ~ 27 + 1(1개 없음)
JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

# 한글 여부 check 후 종성 있는지 체크
def jongsung_check(keyword):
    if re.match('.*[ㄱ-ㅎㅏ-ㅣ가-힣]+.*', keyword) is not None:
        char_code = ord(keyword) - BASE_CODE
        char1 = int(char_code / CHOSUNG)
        char2 = int((char_code - (CHOSUNG * char1)) / JUNGSUNG)
        char3 = int((char_code - (CHOSUNG * char1) - (JUNGSUNG * char2)))
        if char3 == 0:
            return 'F'
        else:
            return 'T'
    else:
        return 'F'


def check_dir(create_path):
    if os.path.exists(create_path):
        return 'already exists'
    else:
        os.mkdir(create_path)
        return 'dir create'


def remove_all_file(dir_path):
    if os.path.exists(dir_path):
        for entry in os.scandir(dir_path):
            if entry.is_file():
                os.remove(entry.path)
        return 'remove all file'
    else:
        return 'directory not found'


# 사전 데이터 파일 생성 함수
def mecab_dic_make(file):
    df = pd.read_csv(file, header=None, names=['name'], encoding='utf-8')
    df['t0'] = None
    df['t1'] = None
    df['t2'] = None
    df['tag'] = 'NNP'
    df['meaning'] = '*'

    df['jongsung'] = [jongsung_check(t[-1]) for t in list(df['name'])]
    df['readname'] = df['name']
    for i in range(5):
        df['s'+str(i)] = '*'

    df.to_csv('data/nnp.csv', mode='w', index=False, header=False, encoding='utf-8')


# 이미 명사로 사전에 등록된 단어는 사전 제작용 파일에서 제외한 새 파일 생성
def pre_dic_check(file):
    df = pd.read_csv(file, header=None, names=['name'], encoding='utf-8')
    tag_list = [npf.get_pos(t) for t in list(df.iloc[:, 0])]
    df['tag'] = tag_list

    del_check = []
    for t in tag_list:
        # 이미 해당 단어가 명사로 등록되어 있는 경우
        if len(t) == 1 and t[0][1][:1] == 'N':
            del_check.append(True)
        else:
            del_check.append(False)

    # 위 조건에 따라 추가로 명사로 등록할 필요가 없는 경우 삭제
    df['del_check'] = del_check
    del_idx = df[df['del_check'] == True].index
    df = df.drop(del_idx)
    df.drop('del_check', axis=1, inplace=True)

    df.to_csv('data/pic_pre_data_check_1.csv', mode='w', index=False, header=False, encoding='utf-8')
    df.drop('tag', axis=1, inplace=True)
    df.to_csv('data/pic_pre_data_check_2.csv', mode='w', index=False, header=False, encoding='utf-8')


def lda(texts, lda_filename):
    # 사전 만들기
    dictionary = corpora.Dictionary(texts)

    # 코퍼스 만들기(벡터화)
    corpus = [dictionary.doc2bow(text) for text in texts]
    # print('corpus : {}'.format(corpus))

    # 모델 구축
    lda = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=1, random_state=1)

    # 주제마다 출현 확률이 높은 단어 순으로 출력
    for t in lda.show_topics():
        print(t)

    # 윈도우 OS의 폰트 경로 예시
    # font_path = 'C:/Windows/Fonts/malgun.ttf';
    # 우분투 OS의 폰트 경로 예시
    # font_path = '/Library/Fonts/AppleGothic.ttf'
    wc = WordCloud(background_color='white', font_path='/System/Library/Fonts/AppleSDGothicNeo.ttc')

    plt.figure(figsize=(30,30))
    for t in range(lda.num_topics):
        plt.subplot(5,4,t+1)
        x = dict(lda.show_topic(t,200))
        im = wc.generate_from_frequencies(x)
        plt.imshow(im)
        plt.axis('off')
        plt.title('Topic #' + str(t))

    # 이미지 저장
    plt.savefig(lda_filename, bbox_inches='tight')

    
def lda_make(open_file_name, start_date, end_date):
    df = pd.read_csv(open_file_name, encoding='utf-8')
    save_file_name = 'output/lda_' + start_date + '~' + end_date + '.png'

    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')

    df['date_created'] = pd.to_datetime(df['date_created']) # df['date_created'] = df['date_created'].astype('datetime64[ns]')
    df = df[(df['date_created'] >= start_date) & (df['date_created'] <= end_date)]

    if df.empty:
        print('해당 기간의 데이터가 없습니다.', start_date + '~' + end_date)
        return
    
    texts = np.array(df['content'])
    np_list = []
    for t in texts:
        np_list.append(npf.np_mecab(t))

    lda(np_list, save_file_name)
    print('lda 저장 완료')


if __name__ == '__main__':
    pass

    # 사전 관련 작업
    # pre_dic_check('data/pic_pre_data.csv')
    # mecab_dic_make('data/pic_pre_data.csv')
    
