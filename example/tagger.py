# -*- coding: utf-8 -*-

# 품사 태깅 실습
# 꼬꼬마와 트위터 형태소 분석기 사용해서 토큰화 수행. 명사 등을 추출한다.

from konlpy.tag import Kkma
kkma = Kkma()

print('kkma 문장분리 : ', kkma.sentences(u'안녕하세요. 반갑습니다. 저는 인공지능입니다.'))
# sentences : 문장분리
print('kkma 명사만추출 : ', kkma.nouns(u'을지로 3가역 주변 첨단빌딩숲 사이에 자리 잡은 커피집'))
# nouns : 명사 추출

print('='*80)

from konlpy.tag import Twitter
tagger = Twitter()

print('Twitter 명사만 추출 : ', tagger.nouns(u'을지로 3가역 주변 첨단빌딩숲 사이에 자리 잡은 커피집'))
print('Twitter 품사 추출 : ', tagger.pos(u'이것도 처리되나욕ㅋㅋ')) # pos : 품사 부착(Part-of-speech tagging)
print('Twitter 오타와 원형처리 : ', tagger.pos(u'이것도되나욕ㅋㅋ', norm=True, stem=True))  # nouns : 명사 추출, norm=True.. 단어의 오타를 자동 정정, stem=True.. '이다'처럼 원형을 리턴. 기본값은 False
