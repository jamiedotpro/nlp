# -*- coding: utf-8 -*-

# 모델을 읽어서 유사도를 구하는 코드
# 여기서 불러오는 모델은 train.py 에서 생성한 모델이다.

from gensim.models import word2vec
import sys

# 첫 번째 파라미터는 사용할 모델 파일 이름
# model = word2vec.Word2Vec.load(sys.argv[1])
model = word2vec.Word2Vec.load('sample.model')
results = model.most_similar(positive=['woman', 'king'], negative=['man'], topn=1)

for result in results:
    print(result[0], '\t', result[1])
