# -*- coding: utf-8 -*-

import crawler_manager
import time, datetime
import pandas as pd
import re

from bs4 import BeautifulSoup


class DaumCrawler(crawler_manager.CrawlerManager):

    def post_list_get(self, post_address, page_num):
        self.driver.get(post_address)
        bs = BeautifulSoup(self.driver.page_source, 'html.parser')

        # 현재 페이지 번호
        curr_page_num = 1
        if post_address.find('&page=') > -1:
            curr_page_num = post_address[post_address.find('&page=') + len('&page='):]

        paging_board = bs.select('div.paging_board')
        if len(paging_board) == 0:
            # 마지막 페이지까지 빈 페이지인 경우 종료
            return pd.DataFrame(None), -1, None
        else:
            paging_board = paging_board[0]
            
        paging_nav = paging_board.select('a')

        next_page_link = 0
        for i in range(1, len(paging_nav)-1):
            if int(paging_nav[i].text.strip()) == int(curr_page_num) + 1:
                next_page_link = paging_nav[i]['href']
                break
        
        if next_page_link == 0:
            next_page_link = paging_nav[len(paging_nav)-1]['href']

        bs = bs.select('#slideArticleList > ul > li')

        data = []
        for i in range(len(bs)):
            # 공지는 읽지 않고 넘어간다
            if 'notice' in bs[i].attrs['class']:
                continue

            post_idx = bs[i].select('a')[0]['href'].strip().split('/')[-1]
            title = bs[i].select('span.txt_detail')[0].text.strip()
            address = self.base_url + bs[i].select('a')[0]['href'].strip()
            # writer = bs[i].select('span.username')[0].text.strip()    # 모바일 페이지에서는 ..으로 줄여서 표시됨. 본문에서 가져온다
            date_created = '20' + bs[i].select('span.created_at')[0].text.strip() + '.'
            date_created = date_created[:4] + '-' + date_created[5:7] + '-' + date_created[8:10]
            
            view = bs[i].select('span.view_count')[0].text.strip()
            recommendation = 0

            # 일정 기간 데이터만 읽어오기
            check_period = crawler_manager.period_check(date_created, self.start_date, self.end_date)
            if check_period == -1:  # 기간 전의 날짜
                break
            elif check_period == 1: # 기간 후의 날짜. 데이터를 계속 읽어와서 이전 날짜 데이터를 가져와야 함
                continue
            
            content, writer = self.post_content_get(address)

            _data = {'post_idx': post_idx, 'title': title, 'content': content, 'date_created': date_created,
                    'writer': writer, 'views': view, 'recommendation': recommendation}

            data.append(_data)

        df = pd.DataFrame(data)

        next_page_link = self.base_url + next_page_link

        return df, check_period, next_page_link


    def post_content_get(self, post_url):
        self.driver.get(post_url)
        bs = BeautifulSoup(self.driver.page_source, 'html.parser')

        content = bs.select('#article')[0].text.strip()
        content = re.sub('"', "'", content)
        content = re.sub('\n', ' ', content)

        writer = bs.select('span.txt_subject')[0].text.strip()
        writer = writer[3:writer.find('|')]
        writer = re.sub('"', "'", writer)

        return content, writer


    def __str__(self):
        return 'DaumCrawler'