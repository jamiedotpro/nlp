# -*- coding: utf-8 -*-

# 영화 데이터(한글)로 단어 임베딩 수행

import codecs
# KoNlpy 0.5.0 버전 이후부터 이름이 Twitter에서 Okt로 바뀌었다.
from konlpy.tag import Twitter
from gensim.models import word2vec
from konlpy.utils import pprint

# 파일 읽기 함수. 첫줄 헤더를 제외하고 한 줄씩 읽어서 data에 담아서 리턴 한다.
def read_data(filename):
    with codecs.open(filename, encoding='utf-8', mode='r') as f:
        data = [line.split('\t') for line in f.read().splitlines()]
        data = data[1:] # header 제외
    return data

# 파일 위치. 본인 파일 경로로 변경해야 함.
ratings_train = read_data('nsmc-master/ratings_train.txt')
# koNlpy 중에서 트위터 형태소 분석기 사용
tw_tagger = Twitter()

# 토크나이즈(의미단어검출) 함수. 트위터 형태소 분석기 사용
# 형태소 / 품사 형태로 리스트화
def tokens(doc):
    return ['/'.join(t) for t in tw_tagger.pos(doc, norm=True, stem=True)]

# 파일 중에서 영화 리뷰 데이터만 담기
docs = []
for row in ratings_train:
    docs.append(row[1])

data = [tokens(d) for d in docs]

# [TRAIN] word2vec으로 모델 생성
w2v_model = word2vec.Word2Vec(data)

# init_sims 명령어로 필요없는 메모리 반환
w2v_model.init_sims(replace=True)

# [TEST] 가장 유사한 단어 출력
pprint(w2v_model.wv.most_similar(positive=tokens(u'남자 여배우'), negative=tokens(u'배우'), topn=1))
