import requests
import pandas as pd
from bs4 import BeautifulSoup

all_news_list = list()


def get_site_map(sitemap_url, start_at):
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

    for x in range(start_at, len(monthly_list)):
        print("-------------------------------------------")
        print("getting monthly news ", x, " of", len(monthly_list))
        get_monthly_news(monthly_list[x], x)


def get_monthly_news(url, i):
    response = requests.get(url)
    response_xml_as_string = response.content.decode('utf-8', errors="replace")
    soup = BeautifulSoup(response_xml_as_string, 'xml')

    monthly_news_list = list()
    monthly_df = pd.DataFrame([])

    start = url.find('monthly-')
    end = url.find('.xml', start)
    date = url[start:end]

    for url_tag in soup.find_all('loc'):
        if "jpg" in url_tag.contents[0]:
            continue
        else:
            monthly_df = monthly_df.append(pd.DataFrame({'Url': url_tag.contents[0],'Date':date}, index=[0]), ignore_index=True)
            # monthly_df['Month'] = date
            monthly_news_list.append(url_tag.contents[0])

    all_news_list.append(monthly_news_list)
    print(monthly_news_list)
    print("Number of Total Monthly Articles ", len(monthly_news_list))
    save_url_csv(monthly_df, i)


def save_url_csv(dataframe, i):
    root = "sitemap"
    print(dataframe.head())
    filename = "thairath_news_" + str(i) + ".csv"
    dataframe.to_csv(root + '/' + filename, index=False, encoding='utf-8')


get_site_map("https://www.thairath.co.th/sitemap.xml", 40)

