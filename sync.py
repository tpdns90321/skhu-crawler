from gevent.monkey import patch_all
patch_all()
import gevent
from gevent.pool import Pool,Group
from gevent.queue import Queue
import json
import redis

from CrawlingBoard import crawlingPage,requestPage,lastPage

# 읽기,쓰기를 각 rw_workers개수로 크롤링 후 레디스 저장을 동시처리하는 클래스
class Sync:
    def __init__(self, Settings, BoardCode):
        workers = Settings["rw-workers"]
        self.readPool = Pool(workers)
        self.writePool = Group()
        self.ch = Queue()
        self.rClient = redis.Redis(host=Settings["redis"],
                                   port=Settings["redis-port"],
                                   password=Settings["redis-password"],
                                   db=BoardCode["dbid"])
        self.bsid = BoardCode["bsid"]
        self.bun = BoardCode["bun"]

    def _Parsing(self, pageNum):
        for article in crawlingPage(pageNum, self.bsid, self.bun):
            self.ch.put(article)

    def _Store(self):
        while True:
            article = self.ch.get()
            if article is None:
                break
            article_num = article[0]
            article_data = json.dumps(article[1:5]).encode("utf-8")
            self.rClient.set(article_num, article_data)

    def firstRun(self):
        self.readPool.map(self._Parsing,
                          range(1,lastPage(requestPage(1,self.bsid,self.bun))+1))
        for _ in range(20):
            self.writePool.add(gevent.spawn(self._Store))
        self.readPool.join()
        for _ in range(20):
            self.ch.put(None)
        self.writePool.join()

    def Run(self):
        if self.rClient.keys().count() == 0:
            self.firstRun()
            return
        raise NotImplementedError
