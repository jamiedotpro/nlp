# -*- coding: utf-8 -*-

import konlpy
import nltk
import pandas as pd
import numpy as np
import re


def stopword(word_list, file='data/stopwords.csv', file2='data/stopwords_cus.csv'):
    df = pd.read_csv(file, encoding='utf-8')
    df2 = pd.read_csv(file2, encoding='utf-8')
    stop_words = list(df['stopwords'])
    stop_words.extend(list(df2['stopwords']))

    result = []
    for word in word_list:
        if word not in stop_words:
            result.append(word)

    return result


def get_pos(sentence, tag_type='mecab'):
    if tag_type == 'okt':
        tagpak = konlpy.tag.Okt()
    else:
        tagpak = konlpy.tag.Mecab()

    # print(tagpak.morphs(u'영등포구청역에 있는 맛집 좀 알려주세요.'))
    # print(tagpak.nouns(u'우리나라에는 무릎 치료를 잘하는 정형외과가 없는가!'))
    # print(tagpak.pos(u'우리나라에는 무릎 치료를 잘하는 정형외과가 없는가!'))
    # print(tagpak.nouns(sentence))

    return tagpak.pos(sentence)


def np_mecab(sentence):
    #!! 형태소 태깅 전에 불용어를 미리 제거하는게 나을듯
    words = konlpy.tag.Mecab().pos(sentence)

    # Define a chunk grammar, or chunking rules, then chunk
    # NNG	일반 명사
    # NNP	고유 명사
    # NNB	의존 명사   x
    # NNBC	단위를 나타내는 명사
    # NR	수사
    # NP	대명사  x

    # XSN	명사파생 접미사
    # XSV	동사 파생 접미사
    # XSA	형용사 파생 접미사

    # JKG   관형적 조사 x 코'의' 상처
	

    # 쓰지 않을 형태소 미리 제거
    words = [w for w in words if w[1] not in ['NNB', 'NP']]
    words = [w for w in words if 'NNB+' not in w[1]]

    # 명사구 규칙
    # 명사 + 명사 + ..., 초등 학교 취학 전 자녀
    # 명사 + 숫자 + 명사, 만 6 세 이하
    # 명사 + 접미사
    # m_np: {<N.*>+<XSN>+|<NNP>*|<N.*>*|<N.*>*<SN>+<N.*>+|<N.*>+<J.*>+<N.*>+}
    # m_np: {<NNP>*|<N.*>*|<N.*>*<SN>+<N.*>+}
    # m_np: {<NNP>|<N.*>*|<N.*>*<SN>+<N.*>+}
    grammar = """
    m_np: {<NNP>|<N.*>*|<N.*>*<SN>+<N.*>+}
    """
    parser = nltk.RegexpParser(grammar)
    chunks = parser.parse(words)

    # print('new sentence-----------------------------')
    # print(sentence)
    # print("# Print whole tree")
    # print(chunks.pprint())

    np_list = []
    # print("\n# Print noun phrases only")
    for subtree in chunks.subtrees():
        if subtree.label() == 'm_np':
            li = ''.join((e[0] for e in list(subtree)))
            np_list.append(li)
            # print(li)
            # print(subtree.pprint())

    # Display the chunk tree
    # chunks.draw()

    np_list = stopword(np_list)

    return np_list


if __name__ == '__main__':
    text = '동해물과 백두산이 마르고 닳도록'

    noun_list = get_pos(text)
    print('\n명사 추출:\n', noun_list)

    np_list = np_mecab(text)
    print('\n명사구 추출_mecab:\n', np_list)
