# -*- coding: utf-8 -*-

import crawler_manager
import time, datetime
import pandas as pd
import re

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup


class NaverCrawler(crawler_manager.CrawlerManager):

    def post_list_get(self, post_address, page_num):
        req = Request(post_address)
        res = urlopen(req)
        html = res.read().decode('CP949')

        bs = BeautifulSoup(html, 'html.parser')

        # 공지를 제외한 나머지를 가져온다.
        bs = bs.select('tbody')[1]

        post_idx = bs.select('div.inner_number')
        titles = bs.select('a.article')
        address = bs.select('a.article')
        writer = bs.select('td.td_name')
        date_created = bs.select('td.td_date')
        views = bs.select('td.td_view')
        recommendation = bs.select('td.td_likes')

        data = []
        for i in range(len(post_idx)):
            _post_idx = post_idx[i].text.strip()

            _title = titles[i].text.strip().split('\n')[0]
            _title = re.sub('"', "'", _title)

            _content = 'https://cafe.naver.com' + address[i]['href']
            _content = self.post_content_get(_content)

            _writer = writer[i].text.strip()
            _writer = _writer[:_writer.find('wordBreak($(')].strip()

            _date_created = crawler_manager.remove_tag(date_created[i].text.strip())
            _date_created = _date_created[:4] + '-' + _date_created[5:7] + '-' + _date_created[8:10]

            _view = views[i].text.strip()
            _recommendation = recommendation[i].text.strip()

            # 일정 기간 데이터만 읽어오기
            check_period = crawler_manager.period_check(_date_created, self.start_date, self.end_date)
            if check_period == -1:  # 기간 전의 날짜
                break
            elif check_period == 1: # 기간 후의 날짜. 데이터를 계속 읽어와서 이전 날짜 데이터를 가져와야 함
                continue

            _data = {'post_idx': _post_idx, 'title': _title, 'content': _content,
                    'date_created': _date_created, 'writer': _writer, 'views': _view, 'recommendation': _recommendation}

            data.append(_data)

        df = pd.DataFrame(data)

        # 첫페이지는 페이지 번호 없이 들어온다.
        # 다음 페이지를 읽기 위해 현재 페이지+1 해서 리턴
        if page_num == 1:
            next_page_link = post_address + '&search.boardtype=L&search.page=' + str(page_num+1)
        else:
            page_num_len = len(post_address) - post_address.find('.page=') - len('.page=')
            next_page_link = post_address[:-page_num_len] + str(page_num+1)

        return df, check_period, next_page_link


    def post_content_get(self, post_url):
        self.driver.get(post_url)
        self.driver.switch_to.frame('cafe_main')
        bs = BeautifulSoup(self.driver.page_source, 'html.parser')
        content = bs.select('#tbody')[0].get_text().strip()
        content = re.sub('"', "'", content)
        content = re.sub('\n', ' ', content)

        return content

        
    def __str__(self):
        return 'NaverCrawler'