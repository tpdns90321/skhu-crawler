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

# # 레디스 디비를 초기화시켜주는 구문
# r=redis.StrictRedis(host='localhost',port=6379)
# r.flushall()
#
# #리스트 선언
# board=[]
#
# #크롤링 한 데이터를 0번 보드에 맞춰서 레디스에 넣는 작업
# r = redis.StrictRedis(host='localhost', port=6379, db=0)
# board = crawlingBoard(10004,51)
# for i in range(0,len(board)):
#     r.set(board[i][0],json.dumps(board[i]))
#
# #크롤링 한 데이터를 1번 보드에 맞춰서 레디스에 넣는 작업
# r = redis.StrictRedis(host='localhost', port=6379, db=1)
# board = crawlingBoard(10005, 53)
# for i in range(0,len(board)):
#     r.set(board[i][0], json.dumps(board[i]))
#
# #크롤링 한 데이터를 2번 보드에 맞춰서 레디스에 넣는 작업
# r = redis.StrictRedis(host='localhost', port=6379, db=2)
# board = crawlingBoard(10038, 39)
# for i in range(0,len(board)):
#     r.set(board[i][0], json.dumps(board[i]))
#
# #크롤링 한 데이터를 3번 보드에 맞춰서 레디스에 넣는 작업
# r = redis.StrictRedis(host='localhost', port=6379, db=3)
# board = crawlingBoard(10006, 75)
# for i in range(0,len(board)):
#     r.set(board[i][0], json.dumps(board[i]))
#
# #크롤링 한 데이터를 4번 보드에 맞춰서 레디스에 넣는 작업
# r = redis.StrictRedis(host='localhost', port=6379, db=4)
# board = crawlingBoard(10007, 0)
# for i in range(0,len(board)):
#     r.set(board[i][0], json.dumps(board[i]))
#
# #크롤링 한 데이터를 5번 보드에 맞춰서 레디스에 넣는 작업
# r = redis.StrictRedis(host='localhost', port=6379, db=5)
# board = crawlingBoard(10008, 0)
# for i in range(0,len(board)):
#     r.set(board[i][0], json.dumps(board[i]))


#게시판 0번의의 글을 가져와서 출력하는 구문
#r=redis.StrictRedis(host='localhost',port=6379, db=0)
#for i in range(1, len(crawlingBoard(10004, 51))):
#    print(r.get(str(i)))


#게시판의 i번째 페이지의 글을 가져오는 구문
# print(crawlingPage(1,10004,51))

#모든 데이터베이스의 모든 키값들을 없애는 명령어
# FLUSHALL

#현재 데이터베이스의 모든 키값들을 없애는 명령어
# FLUSHDB

# r.set()


