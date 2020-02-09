# -*- coding: utf-8 -*-

from abc import *
import platform
import os
import re
import pyperclip
import time, datetime
import pandas as pd

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class CrawlerManager(metaclass=ABCMeta):

    def __init__(self, driver, data, start_date, end_date):
        self.driver = driver

        self.start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        self.end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')

        self.user_id = data['user_id']
        self.user_pw = data['user_pw']

        self.login_url = data['login_url']
        self.id_ele_xpath = data['id_ele_xpath']
        self.pw_ele_xpath = data['pw_ele_xpath']
        self.btn_ele_xpath = data['btn_ele_xpath']

        self.base_url = data['base_url']
        self.board_id_tag = data['board_id_tag']
        self.board_id_list = data['board_id_list']

        # save_df_name + '시작날짜', + _post_ + board_id + .csv
        self.save_df_name = data['save_df_name']


    # 네이버는 아이디, 패스워드를 직접 입력하면 CAPTCHA 입력창이 뜨기 때문에, 붙여넣기로 입력함
    # 다음은 다른 태그로 감싸져 있어 아이디/비번 입력 위치 클릭이 안됨. 엔터로 변경
    def copy_input(self, xpath, input):
        pyperclip.copy(input)
        # self.driver.find_element_by_xpath(xpath).click()
        self.driver.find_element_by_xpath(xpath).send_keys(Keys.ENTER)

        if 'Windows' == platform.system():
            ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()  # windows
        else:
            ActionChains(self.driver).key_down(Keys.COMMAND).send_keys('v').key_up(Keys.COMMAND).perform()  # mac


    def login_process(self):
        if self.login_url == None:
            print('login_process pass')
            return
        else:
            print('login_process start')

        self.driver.implicitly_wait(3)
        self.driver.get(self.login_url)
        time.sleep(3)

        self.copy_input(self.id_ele_xpath, self.user_id)
        self.copy_input(self.pw_ele_xpath, self.user_pw)
        self.driver.find_element_by_xpath(self.btn_ele_xpath).click()
        time.sleep(3)


    def crawler_save_check(self, text):
        print(text)
        with open('crawler_save_check.txt', mode='a', encoding='utf-8') as f:
            f.write(text)


    def post_get(self):
        print('post_get start')

        df_post = None
        next_page_link = None
        start_page = 1
        for board_id in self.board_id_list:
            for i in range(start_page, 10000):
                # 1페이지부터 진행하다가 날짜가 넘어가면 패스할 예정
                if i == start_page:
                    post_address = self.base_url + self.board_id_tag + board_id
                else:
                    post_address = next_page_link

                df_post_add, check_period, next_page_link = self.post_list_get(post_address, i)

                if df_post_add.empty and check_period < 0:
                    progress_text = '='*20 + '\n'
                    progress_text += 'time:' +  str(datetime.datetime.now()) +  '\n'
                    progress_text += '해당 게시판 데이터 읽기 완료\n'
                    self.crawler_save_check(progress_text)
                    break

                if i == start_page:
                    df_post = df_post_add
                else:
                    df_post = pd.concat([df_post, df_post_add])

                progress_text = '='*20 + '\n'
                progress_text += 'time:' +  str(datetime.datetime.now()) +  '\n'
                progress_text += 'board_id: ' + str(board_id) + ' page: ' + str(i) + '\n'
                self.crawler_save_check(progress_text)

                save_file_name = self.save_df_name + str(self.start_date.strftime('%Y-%m-%d')) + '_post_' + board_id + '.csv'
                df_post.to_csv(save_file_name, mode='w', index=False, encoding='utf-8')


    @abstractmethod
    def post_list_get(self, post_address):
        pass


    @abstractmethod
    def post_content_get(self, post_url):
        pass


    @abstractmethod
    def __str__(self):
        pass



def remove_tag(text):
    cleaner = re.compile('<.*?>')
    text = re.sub(cleaner, '', text)
    text = re.sub('&nbsp;', ' ', text)
    return text


def period_check(check_date, start_date, end_date):
    # 날짜 포맷이 안 맞다면, 당일에 올라온 데이터
    # 이전의 데이터만 읽을 것이므로, 기간 후의 데이터로 둔다.
    if ':' in check_date or '전' in check_date or '방금' in check_date:
        return 1
        
    check_date = datetime.datetime.strptime(check_date, '%Y-%m-%d')

    if check_date >= start_date:
        if check_date <= end_date:
            return 0    # 기간 안에 포함됨
        else:
            return 1    # 기간 후의 날짜
    else:
        return -1       # 기간 전의 날짜
