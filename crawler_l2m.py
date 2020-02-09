# -*- coding: utf-8 -*-

import crawler_manager
import time, datetime
import pandas as pd
import re

from bs4 import BeautifulSoup


class L2mCrawler(crawler_manager.CrawlerManager):

    def post_list_get(self, post_address, page_num):
        self.driver.get(post_address)
        bs = BeautifulSoup(self.driver.page_source, 'html.parser')

        return


    def post_content_get(self, post_url):
        self.driver.get(post_url)
        bs = BeautifulSoup(self.driver.page_source, 'html.parser')

        return


    def __str__(self):
        return 'Lineage2mCrawler'