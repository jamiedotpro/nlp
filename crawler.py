# -*- coding: utf-8 -*-

# 네이버 건강 포스트
# https://post.naver.com/subject/list.nhn?navigationType=push&categoryNo=31&subjectType=CATEGORY&mainMenu=HEALTH

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re
import pandas as pd


def remove_tag(text):
    cleaner = re.compile('<.*?>')
    text = re.sub(cleaner, '', text)
    text = re.sub('&nbsp;', ' ', text)
    return text


def get_content(address):
    req = Request(address)
    res = urlopen(req)
    html = res.read().decode('utf-8')

    bs = BeautifulSoup(html, 'html.parser')
    raw_contents = bs.text.split('\n')
    text = ''
    for rc in raw_contents:
        rc = rc.strip()
        if rc[:23] == '<p class="se_textarea">':
            rc = remove_tag(rc)
            if rc != '':
                text += ' ' + rc

    return text.strip()


def board_parse():
    req = Request('https://post.naver.com/subject/list.nhn?navigationType=push&categoryNo=31&subjectType=CATEGORY&mainMenu=HEALTH')
    res = urlopen(req)
    html = res.read().decode('utf-8')

    bs = BeautifulSoup(html, 'html.parser')
    # tags = bs.find('ul', attrs={'class': 'list_box list_spot_post'})

    titles = bs.select('div.spot_post_name')
    dates = bs.select('p.spot_post_date')
    address = bs.select('li > a.spot_post_area')

    contents = []
    for i in range(len(titles)):
        titles[i] = titles[i].text.strip()
        titles[i] = re.sub('\n', ' ', titles[i])
        dates[i] = dates[i].text[:11]
        address[i] = 'https://post.naver.com' + address[i]['href']
        # print(dates[i] + ' / ' + titles[i] + ' / ' + address[i])
        contents.append(get_content(address[i]))

    data = {'dates': dates, 'titles': titles, 'address': address, 'contents': contents}

    return data


if __name__ == '__main__':
    board_data = board_parse()
    df_board_data = pd.DataFrame(board_data)
    df_board_data.to_csv('board_data.csv', mode='w', index=False, encoding='utf-8')

    # for i in range(len(board_data['dates'])):
    #     print(board_data['dates'][i] + ' / ' + board_data['titles'][i] + ' / ' + board_data['address'][i])
    #     print(board_data['contents'][i])
