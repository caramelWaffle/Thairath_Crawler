import requests
import os
import sys
import pandas as pd
from bs4 import BeautifulSoup

all_news_list = list()


def get_site_map(sitemap_url):
    monthly_list = list()
    response = requests.get(sitemap_url)
    response_xml_as_string = response.content.decode('utf-8', errors="replace")
    soup = BeautifulSoup(response_xml_as_string, 'xml')
    for url_tag in soup.find_all('loc'):
        news_url = url_tag.contents[0]
        if "monthly" not in url_tag.contents[0]:
            continue
        else:
            monthly_list.append(url_tag.contents[0])

    print("Total month : ", len(monthly_list))
    i = 1
    for monthly_url in monthly_list:
        print("-------------------------------------------")
        print("getting monthly news ", i, " of", len(monthly_list))
        get_monthly_news(monthly_url)
        i = i+1


def get_monthly_news(url):
    response = requests.get(url)
    response_xml_as_string = response.content.decode('utf-8', errors="replace")
    soup = BeautifulSoup(response_xml_as_string, 'xml')

    monthly_news_list = list()
    monthly_df = pd.DataFrame([])

    start = url.find('monthly-')
    end = url.find('.xml', start)
    filename = url[start:end]

    for url_tag in soup.find_all('loc'):
        if "jpg" in url_tag.contents[0]:
            continue
        else:
            monthly_df = monthly_df.append(pd.DataFrame({'Url': url_tag.contents[0], 'Parent': filename}, index=[0]), ignore_index=True)
            monthly_news_list.append(url_tag.contents[0])

    all_news_list.append(monthly_news_list)
    print(monthly_news_list)
    print("Number of Total Monthly Articles ", len(monthly_news_list))
    save_url_csv(monthly_df, filename)


def save_url_csv(dataframe, filename):
    print(dataframe.head())
    filename = "thairath_news_" + filename + ".csv"
    dataframe.to_csv("sitemap" + '/' + filename, sep='\t', encoding='utf-8')


get_site_map("https://www.thairath.co.th/sitemap.xml")

