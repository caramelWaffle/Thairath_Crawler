# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.crawler import CrawlerProcess

from ..items import ThairathSpiderItem
import os
import glob
import pandas as pd

path = "E:\Khun Projects\Thairath_Crawler\sitemap\\"
file_name = "3rd_batch"


class ThairathTabletsSpider(scrapy.Spider):
    name = 'thairath_spider'
    allowed_domains = ['thairath.co.th']
    extension = '.csv'
    file_name = file_name + extension
    data = pd.read_csv(path + file_name)
    start_urls = data["Url"].values

    def make_requests_from_url(self, url):
        return Request(url, dont_filter=True, meta={
            'dont_redirect': True,
            'handle_httpstatus_list': [301, 302]
        })

    def parse(self, response):
        # Get Title
        title = response.xpath("//meta[@property='og:title']/@content")[0].extract()

        # Get URL
        url = response.xpath("//meta[@property='og:url']/@content")[0].extract()

        # Get Published Date
        date = response.xpath("//meta[@property='og:article:published_time']/@content")[0].extract()

        # Get Meta_Sum
        meta_sum = response.xpath("//meta[@name='description']/@content").extract()

        # Get News Type
        type = response.css(".css-7enauw a::text").extract()

        # Get art_sum
        article_sum = response.css(".evs3ejl35 strong::text, .evs3ejl35 p strong::text").extract()

        # Get Body
        body = response.css(".evs3ejl1 p::text, .evs3ejl1 p strong::text,.evs3ejl1 strong::text, .evs3ejl1 a::text, .evs3ejl1 h2::text, .evs3ejl1 h2 u::text").extract()

        # Get Tags
        tags = response.css(".evs3ejl16 a::text").extract()

        items = ThairathSpiderItem()
        items['title'] = title
        items['url'] = url
        items['date'] = date
        items['meta_sum'] = meta_sum
        items['type'] = type
        items['article_sum'] = article_sum
        items['body'] = body
        items['tags'] = tags
        yield items
