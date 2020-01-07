# -*- coding: utf-8 -*-

# 서포트 벡터 머신 모델을 이용한 감정 분석

from konlpy.tag import Twitter
from pprint import pprint
import nltk # 서포트 벡터 머신 모델 구현을 위한 API
from sklearn.svm  import LinearSVC
from nltk.classify.scikitlearn import SklearnClassifier

# 파일에서 데이터 읽어오기
def read_data(filename):
    with open(filename, 'r', encoding='utf8') as f:
        data = [line.split('\t') for line in f.read().splitlines()]
        data = data[1:] # header 제외
    return data

train_data = read_data('nsmc-master/ratings_train.txt')
test_data = read_data('nsmc-master/ratings_test.txt')    # id, text, sentiment

# Data 개수 확인
print(len(train_data))  # train_data : 150,000
print(len(train_data[0]))   # 변수 : id, text, sentiment

print(len(test_data))   # test_data : 50,000
print(len(test_data[0]))    # 변수 : id, text, sentiment

# KoNlpy의 트위터 형태소 분석기를 통한 토큰화
pos_tagger = Twitter()

def tokenize(doc):
    return['/'.join(t) for t in pos_tagger.pos(doc, norm=True, stem=True)]

train_docs = [(tokenize(row[1]), row[2]) for row in train_data]
test_docs = [(tokenize(row[1]), row[2]) for row in test_data]

# Data summary
tokens = [t for d in train_docs for t in d[0]]  # 각 문장별로 토큰화된 리스트를 하나로 합칩
print(len(tokens))
text = nltk.Text(tokens, name='NMSC')

# classification 상위 200개 token만 변수로 사용
selected_words = [f[0] for f in text.vocab().most_common(200)]
def term_exists(doc):
    return {'exists({})'.format(word): (word in set(doc)) for word in selected_words}

train_docs = train_docs[:5000]  # 훈련 시간 단축을 위해 50000개만 사용

train_xy = [(term_exists(d),c) for d,c in train_docs]   # tf matrix랑 비슷한 개념
test_xy = [(term_exists(d),c) for d,c in test_docs]

# 서포트 벡터 머신 학습 및 평가
print('='*20)
print('classifier_SVM : ')
classif = SklearnClassifier(LinearSVC())
classifier_svm = classif.train(train_xy)
print(nltk.classify.accuracy(classifier_svm, test_xy))
print('='*20)
