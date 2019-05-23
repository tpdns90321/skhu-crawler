from gevent.monkey import patch_all
patch_all()
import gevent
from gevent.pool import Pool,Group
from gevent.queue import Queue
import redis

from CrawlingBoard import crawlingPage,requestPage,lastPage
from DBClient import DBClient

# 읽기,쓰기를 각 rw_workers개수로 크롤링 후 레디스 저장을 동시처리하는 클래스
class Sync(DBClient):
    def __init__(self, Settings, BoardCode):
        # 설정값을 통해 초기화를 한다.
        self.workers = Settings["rw-workers"]
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

    # Queue에서 글을 받아서 redis에 저장한다.
    def _Store(self):
        while True:
            article = self.ch.get()
            # 종료 신호가 오면 종료한다.
            if article is None:
                break
            # 글 번호
            article_num = article[0]
            # 글 번호를 제외한 글 자료를 저장한다.
            article_data = article[1:5]
            # DB에 저장
            self.set(article_num, article_data)

    # 처음에 DB가 비어있을 떄 모든 글들을 불러오는 함수이다.
    def firstRun(self):
        # readPool에서 끝 페이지 번호까지 페이지를 파싱한다.
        self.readPool.map(self._Parsing,
                          range(1,lastPage(requestPage(1,self.bsid,self.bun))+1))
        # workers개수로 쓰는 함수를 시작한다.
        for _ in range(self.workers):
            self.writePool.add(gevent.spawn(self._Store))
        # readPool이 끝나길 기다린다.
        self.readPool.join()
        # writePool 개수대로 종료신호를 전달한다.
        for _ in range(self.workers):
            self.ch.put(None)
        # writePool이 끝나기 기달린다.
        self.writePool.join()

    # DB가 비어있으면 firstRun을 실행하고 아니면 갱신만 하면 된다.
    # 미구현 상태
    def Run(self):
        if self.keys().count() == 0:
            self.firstRun()
            return
        raise NotImplementedError
