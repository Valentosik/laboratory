from selenium import webdriver
from lxml.html import fromstring
import json
import time
import datetime
import requests

def get_source_code(agent, url):
  agent.get(url)
  source_code = fromstring(agent.page_source)
  # print(source_code)
  return source_code
# this func goes through 40 pages and gets about 10 links on articles from each page
def get_articles_urls(agent, source_code, links, i):
  temp_list_of_links = (source_code.xpath("//h2[@class='entry-title']/a/@href"))
  # links on articles to be parsed 
  for elem in temp_list_of_links:
    links.append(elem)
  if i != 39:
    # link on next page with other 10 articles
    next_page = source_code.xpath("//*[@id='content']/div[12]/div/a[@class='nextpostslink']/@href")
    return (links, next_page[0])
  return links

if __name__ == '__main__':
    driver = webdriver.Firefox(executable_path='geckodriver',  
                    firefox_binary='/Applications/Firefox Developer Edition.app/Contents/MacOS/firefox-bin')
    url = 'https://www.enterpriseai.news/category/storage/'
    source_code =  get_source_code(driver, url)
    links = []

    for i in range(40):
      if i != 39:
        links, next_page = get_articles_urls(driver, source_code, links, i)
        source_code = get_source_code(driver, next_page)
      else:
        links = get_articles_urls(driver, source_code, links, i)
    driver.quit()
  # all links are put into json file
    article_link_data = {}
    for i in range(394):
      article_link_data[str(i)] = links[i]
    print(len(article_link_data))
    with open('articles.json', 'w', encoding='utf-8') as f:
      json.dump(article_link_data, f, indent=4)

  # now we have links on 394 article and we'll parse them
    

    