import requests
import re
import json
from bs4 import BeautifulSoup

#성공회대학교 URL
URL = "http://skhu.ac.kr/board/"

#페이지의 request 전체를 가져오는 구문
def requestPage(pageNum,bsid,bun):
    req=requests.get(URL + 'boardlist.aspx?curpage={}&bsid={}&searchBun={}'.format(pageNum, bsid, bun))
    source = req.text
    soup = BeautifulSoup(source,'html.parser')
    return soup

#마지막 페이지의 값을 구하는 구문
def lastPage(soup):
    top_list = soup.select("a.nextL")
    endpoint = int(re.findall('curpage=(\d+)', str(top_list[0]))[0])
    return endpoint

#2번째 td의 a태그의 href 값을 구하는 구문
def extractHref(tag):
    return re.sub("amp\;", "",re.findall('([\w=\?\&\.\;]+)',str(tag.a))[2])

# 해당 페이지를 크롤링하는 구문
def crawlingPage(i,bsid,bun):
    page = []
    top_list = requestPage(i, bsid, bun).select("#cont > table > tbody > tr")
    for l in filter(lambda tag: True if tag.td.text != "공지" else False, top_list):
        page.append([int(l.td.text), l.a.text, URL + extractHref(l), l.contents[7].text, l.contents[9].text])
    return page

# 공지를 포함하지 않은 1~마지막 페이지까지의 글 목록
def crawlingBoard(bsid, bun):
    board = []
    for i in range (1,lastPage(requestPage(1, bsid, bun))+1):
        board.extend(crawlingPage(i,bsid,bun))
    return board

