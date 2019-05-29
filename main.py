import gevent
from gevent.pywsgi import WSGIServer
from flask import Flask,request

from settings import generateDefaultSetting
from BoardCode import CODES
from api import API
from sync import Sync

APIS = {}
SYNC = {}

app = Flask(__name__)

@app.route("/")
def index():
    return "SKHU NOTICE CRAWLER"

@app.route("/get/<part>")
def get(part):
    page = request.args.get("page", default = 1, type = int)
    view = request.args.get("view", default = 15, type = int)
    data = APIS[part.upper()].get(page, view)
    res = app.response_class(
            response=data,
            status=200,
            mimetype="application/json")
    return res

def init_class(setting, target):
    res = {}
    for k,v in CODES.items():
        res[k] = target(setting, v)
    return res

if __name__ == "__main__":
    setting = generateDefaultSetting()
    if setting["MODE"] == "api":
        APIS = init_class(setting, API)
        http = WSGIServer(("", 3000), app)
        print("api server start")
        http.serve_forever()
    elif setting["MODE"] == "crawling":
        SYNC = init_class(setting, Sync)
        th = [gevent.spawn(s.Run) for s in SYNC.values()]
        gevent.joinall(th)

