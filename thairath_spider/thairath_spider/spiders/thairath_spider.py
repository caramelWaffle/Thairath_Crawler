# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.crawler import CrawlerProcess

from ..items import ThairathSpiderItem
import os
import glob
import pandas as pd

path = "E:\Khun Projects\Thairath_Crawler\sitemap"
file_name = "thairath_news_"  # Change here 1 (first time)


class ThairathTabletsSpider(scrapy.Spider):
    start_index = "0"  # Change here 2 (every time)
    name = 'thairath_spider'
    allowed_domains = ['thairath.co.th']
    os.chdir(path)
    extension = '.csv'
    # all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    # all_filenames.sort()
    file_name = file_name + str(start_index) + extension
    data = pd.read_csv(path + '\\' + file_name)
    start_urls = data["Url"].values

    def make_requests_from_url(self, url):
        return Request(url, dont_filter=True, meta={
            'dont_redirect': True,
            'handle_httpstatus_list': [301, 302]
        })

    def parse(self, response):
        print("procesing:" + response.url)
        self.log("procesing:" + response.url)
        # Extract data using css selectors
        # Get Title
        title = response.css(".e1ui9xgn0::text").extract()

        # Get Summary
        summary = response.css(".evs3ejl35 p::text,.evs3ejl35 p strong::text,.evs3ejl35 strong::text").extract()

        # Get Body
        body = response.css("div p::text, div p strong::text, div strong::text").extract()

        # Get Tags
        tags = response.css(".evs3ejl16 a::text").extract()

        items = ThairathSpiderItem()
        items['title'] = title
        items['summary'] = summary
        items['body'] = body
        items['tags'] = tags

        yield items
