from gevent.monkey import patch_all
patch_all()
import gevent
from gevent.pool import Pool,Group
from gevent.queue import Queue
import redis

from CrawlingBoard import crawlingPage,requestPage,lastPage
from DBClient import DBClient

ARTICLE_ATTR = ["num", "name", "url", "writer", "date"]

# 읽기,쓰기를 각 rw_workers개수로 크롤링 후 레디스 저장을 동시처리하는 클래스
class Sync(DBClient):
    def __init__(self, Settings, BoardCode):
        # 설정값을 통해 초기화를 한다.
        self.workers = Settings["RW_WORKERS"]
        # 읽기는 Pool로 처리한다. 몇 개가 들어오는지 예측이 불가하기 때문이다.
        self.readPool = Pool(self.workers)
        # 쓰기는 정해진 개수로 처리하므로 Group으로 몪는다.
        self.writePool = Group()
        # readPool 과 writePool 간의 통신을 위한 Queue 클래스
        self.ch = Queue()
        # 보드코드를 저장한다.
        self.bsid = BoardCode["bsid"]
        self.bun = BoardCode["bun"]
        # DB 연결을 시작한다.
        DBClient.__init__(self, Settings, BoardCode)

    # 한 페이지를 크롤링해 글 단위로 Queue로 writePool에 전송한다.
    def _Parsing(self, pageNum):
        for article in crawlingPage(pageNum, self.bsid, self.bun):
            self.ch.put(article)

    # 종료신호를 전달한다.
    def _endSignal(self):
        for _ in range(self.workers):
            self.ch.put(None)

    def _updateParsing(self, last, pageNum):
        # 글을 추출한다.
        for article in crawlingPage(pageNum, self.bsid, self.bun):
            # 글번호가 최근글보다 크면 저장하고 아니면 종료한다.
            if article[0] > last:
                self.ch.put(article)
            else:
                self._endSignal()
                return

        # 다음 글을 읽으려 간다.
        self.readPool.spawn(self._updateParsing,
                            last,
                            pageNum+1)

    def _storeArticle(self, article):
        # 글 번호
        article_num = article[0]
        # 키를 참조해 값과 함께 dictionary로 변환
        article_res = {}
        for k,v in zip(ARTICLE_ATTR, article):
            article_res[k] = v
        # DB에 저장
        self.set(article_num, article_res)

    # Queue에서 글을 받아서 redis에 저장한다.
    def _Store(self):
        while True:
            article = self.ch.get()
            # 종료 신호가 오면 종료한다.
            if article is None:
                break
            self._storeArticle(article)

    # workers개수로 쓰는 함수를 시작한다.
    def writePoolSpawn(self):
        [self.writePool.add(gevent.spawn(self._Store)) for _ in range(self.workers)]

    # 처음에 DB가 비어있을 떄 모든 글들을 불러오는 함수이다.
    def firstRun(self):
        # readPool에서 끝 페이지 번호까지 페이지를 파싱한다.
        self.readPool.map(self._Parsing,
                          range(1,lastPage(requestPage(1,self.bsid,self.bun))+1))
        # workers개수로 쓰는 함수를 시작한다.
        self.writePoolSpawn()
        # readPool이 끝나길 기다린다.
        self.readPool.join()
        # writePool 개수대로 종료신호를 전달한다.
        self._endSignal()
        # writePool이 끝나기 기달린다.
        self.writePool.join()

    # DB가 비어있으면 firstRun을 실행하고 아니면 갱신을 한다.
    def Run(self):
        count = len(self.keys())
        # db가 비어있는지 확인한다.
        if count == 0:
            self.firstRun()
            return

        # 새 글을 찾는 함수를 실행한다.
        self.readPool.spawn(self._updateParsing, count, 1)
        # workers개수로 쓰는 함수를 시작한다.
        self.writePoolSpawn()
        # 끝나기 기달린다.
        self.writePool.join()
