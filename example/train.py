# -*- coding: utf-8 -*-

# word2vec 모델을 만드는 실습 파일
# word2vec : 구글에서 만든 알고리즘. 각 단어 간의 앞뒤 관계를 보고 근접도를 정하는 방식이며, 딥러닝을 통한 비지도학습 알고리즘이다.
#            단어 자체를 벡터화하고, 두 단어 간의 유사성을 확인할수 있는 모델
# 여기서 생성한 모델은 similarity.py 에서 사용한다.

from gensim.models import word2vec
import logging
import sys

# 로그 저장 용도
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# 첫 번째 파라미터는 읽어올 파일의 이름
# sentences = word2vec.LineSentence(sys.argv[1])
sentences = word2vec.LineSentence('text8.txt')

# size: 공간 크기
# min_count: 단어 최저 등장 횟수. 총 빈도가 이보다 작은 모든 단어를 무시한다
# window: 윈도우 수. 문장 내에서 현재 단어와 예측 단어 사이의 최대 거리
model = word2vec.Word2Vec(sentences, size=100, min_count=1, window=10)

# 두 번째 파라미터는 생성할 모델명
# model.save(sys.argv[2])
model.save('sample.model')

# cmd -> python train.py text8.txt sample.model