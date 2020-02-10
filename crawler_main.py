# -*- coding: utf-8 -*-

import platform
import crawler_manager
from crawler_daum import DaumCrawler
from crawler_naver import NaverCrawler
from crawler_l2m import L2mCrawler
from selenium import webdriver


def daum_data():
    user_id = ''
    user_pw = ''

    # 다음 계정
    login_url = 'https://logins.daum.net/accounts/signinform.do?url=https%3A%2F%2Fwww.daum.net%2F'
    id_ele_xpath = '//*[@id="id"]'
    pw_ele_xpath = '//*[@id="inputPwd"]'
    btn_ele_xpath = '//*[@id="loginForm"]/fieldset/button'

    # 카카오 계정
    # login_url = 'https://accounts.kakao.com/login?continue=https%3A%2F%2Faccounts.kakao.com%2Fweblogin%2Faccount'
    # id_ele_xpath = '//*[@id="id_email_2"]'
    # pw_ele_xpath = '//*[@id="id_password_3"]'
    # btn_ele_xpath = '//*[@id="login-form"]/fieldset/div[8]/button'

    base_url = 'https://m.cafe.daum.net'
    board_id_tag = '/dotax/'
    board_id_list = ['OJGx',    # PC 게임게시판
                    'OUVA',     # 모바일 게임 게시판
                    ]

    save_df_name = 'data_c/daum_'
    
    data = {'user_id': user_id, 'user_pw': user_pw, 'login_url': login_url,
        'id_ele_xpath': id_ele_xpath, 'pw_ele_xpath': pw_ele_xpath, 'btn_ele_xpath': btn_ele_xpath,
        'base_url': base_url, 'board_id_list': board_id_list, 'board_id_tag': board_id_tag, 'save_df_name': save_df_name}

    return data
    

def naver_data():
    user_id = ''
    user_pw = ''

    login_url = 'https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com'
    id_ele_xpath = '//*[@id="id"]'
    pw_ele_xpath = '//*[@id="pw"]'
    btn_ele_xpath = '//*[@id="frmNIDLogin"]/fieldset/input'

    base_url = 'https://cafe.naver.com/ArticleList.nhn?search.clubid=10660268'
    board_id_tag = '&search.menuid='
    board_id_list = ['224',     # 모바일 뉴스
                    '1117',     # 모바일 앱
                    ]

    save_df_name = 'data_c/naver_'

    data = {'user_id': user_id, 'user_pw': user_pw, 'login_url': login_url,
        'id_ele_xpath': id_ele_xpath, 'pw_ele_xpath': pw_ele_xpath, 'btn_ele_xpath': btn_ele_xpath,
        'base_url': base_url, 'board_id_list': board_id_list, 'board_id_tag': board_id_tag, 'save_df_name': save_df_name}

    return data


def l2m_data():
    user_id = None
    user_pw = None

    login_url = None
    id_ele_xpath = None
    pw_ele_xpath = None
    btn_ele_xpath = None

    base_url = 'https://lineage2m.plaync.com/board'
    board_id_tag = '&search.menuid='
    board_id_list = ['all/list',            # 전체
                    'free/list',            # 자유
                    'server/list',          # 월드
                    'member_recruit/list',  # 혈맹 모집
                    'qnanknowhow/list',     # 질문&노하우
                    ]

    save_df_name = 'data_c/l2m_'

    data = {'user_id': user_id, 'user_pw': user_pw, 'login_url': login_url,
        'id_ele_xpath': id_ele_xpath, 'pw_ele_xpath': pw_ele_xpath, 'btn_ele_xpath': btn_ele_xpath,
        'base_url': base_url, 'board_id_list': board_id_list, 'board_id_tag': board_id_tag, 'save_df_name': save_df_name}

    return data


if __name__ == '__main__':
    if 'Windows' == platform.system():
        driver = webdriver.Firefox(capabilities=None, executable_path='geckodriver-v0.26.0-win64/geckodriver.exe')
    else:
        # driver = webdriver.Firefox(capabilities=None, executable_path='/usr/local/bin/geckodriver')
        driver = webdriver.Firefox(capabilities=None, executable_path='geckodriver-v0.25.0-macos/geckodriver')

    #!! 기간 내에 게시글이 하나도 없을 때 예외처리 추가 필요
    start_date = '2015-05-01'
    end_date = '2015-05-31'

    crawler_list = [DaumCrawler(driver, daum_data(), start_date, end_date),
                    NaverCrawler(driver, naver_data(), start_date, end_date),
                    # L2mCrawler(driver, l2m_data(), start_date, end_date)
                    ]

    for c in crawler_list:
        print('='*20)
        print('class_name:', c)
        c.login_process()
        c.post_get()

    driver.close()
