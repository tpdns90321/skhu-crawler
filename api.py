import json

from DBClient import DBClient

class Api(DBClient):
    def __INIT__(self, Setting, BoardCode):
        DBClient.__INIT__(self, Setting, BoardCode)

    def get(self, page, perView):
        keys = self.keys(sort=True)
        start = len(keys) - page * perView
        end = len(keys) - (page - 1) * perView
        start = 0 if start < 0 else start
        end = 0 if end < 0 else end
        query = []
        for k in keys[start:end]:
            query.append(DBClient.get(self,k))
        query.reverse()
        return json.dumps(query, ensure_ascii=False)
