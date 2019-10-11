# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

from ..items import ThairathSpiderItem


class ThairathTabletsSpider(scrapy.Spider):
    name = 'thairath_tablets'
    allowed_domains = ['thairath.co.th']
    # start_urls = ['https://www.thairath.co.th/news/crime/1672393']

    start_urls = [
        'https://www.thairath.co.th/news/politic/1507875',
        'https://www.thairath.co.th/news/local/east/1507891',
        'https://www.thairath.co.th/news/politic/1507830'
    ]

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
        summary = response.css(".evs3ejl35 p::text").extract()

        # Get Body
        body = response.css("div p::text").extract()

        # Get Tags
        tags = response.css(".evs3ejl16 a::text").extract()

        items = ThairathSpiderItem()
        items['title'] = title
        items['summary'] = summary
        items['body'] = body
        items['tags'] = tags

        yield items
