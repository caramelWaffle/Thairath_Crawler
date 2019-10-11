# -*- coding: utf-8 -*-
import scrapy


class ThairathTabletsSpider(scrapy.Spider):
    name = 'thairath_tablets'
    allowed_domains = ['thairath.co.th']
    start_urls = ['https://www.thairath.co.th/news/politic/1680358/']

    def parse(self, response):
        print("procesing:"+response.url)
        self.log("procesing:"+response.url)
        # Extract data using css selectors
        # Get Title
        title = response.css(".e1ui9xgn0::text").extract()

        # Get Summary
        summary = response.css(".evs3ejl35 p::text").extract()

        # Get Body
        body = response.css("div p::text").extract()

        # Get Tags
        tags = response.css(".evs3ejl16 a::text").extract()

        row_data = zip(title, summary, body, tags)

        print(summary)

        # Making extracted data row wise
        for item in row_data:
            # create a dictionary to store the scraped info
            scraped_info = {
                # key:value
                'page': response.url,
                'title': item[0],
                # item[0] means product in the list and so on, index tells what value to assign
                'summary': item[1],
                'body': item[2],
                'tags': item[3],
            }
            # yield or give the scraped info to scrapy
            yield scraped_info
