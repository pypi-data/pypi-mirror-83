# -*- coding: utf-8 -*-
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from ltp import LTP

model_path = r"/root/Data/NLP/Model/LTP"

app = FastAPI()

ltp = LTP(path=model_path)


class Item(BaseModel):
    texts: List[str]


class Words(BaseModel):
    words: List[str]
    max_window: int = 4


@app.post("/sent_split")
def sent_split(item: Item):  # 分句
    ret = {
        'texts': item.texts,
        'sents': [],
        "status": 0
    }
    try:
        sents = ltp.sent_split(item.texts)
        ret['sents'] = sents
    except Exception:
        ret['status'] = 1
    return ret


@app.post("/add_words")
def add_words(words: Words):  # 增加自定义词语
    ret = {
        'status': 0
    }
    try:
        ltp.add_words(words=words.words, max_window=words.max_window)
    except Exception:
        ret['status'] = 1
    return ret


@app.post("/seg")
def seg(item: Item):  # 分句
    ret = {
        'status': 0,
        'texts': item.texts,
        'seg': [],
    }
    try:
        seg, hidden = ltp.seg(item.texts)
        ret['seg'] = seg
    except Exception:
        ret['status'] = 1
    return ret


@app.post("/pos")
def pos(item: Item):  # 词性标注
    ret = {
        'status': 0,
        'texts': item.texts,
        'seg': [],
        'pos': []
    }
    try:
        seg, hidden = ltp.seg(item.texts)
        res = ltp.pos(hidden)
        ret['seg'] = seg
        ret['pos'] = res
    except Exception:
        ret['status'] = 1
    return ret


@app.post("/ner")
def ner(item: Item):  # 命名实体识别
    ret = {
        'status': 0,
        'texts': item.texts,
        'seg': [],
        'ner': [],
    }
    try:
        seg, hidden = ltp.seg(item.texts)
        res = ltp.ner(hidden)
        ret['seg'] = seg
        ret['ner'] = res
    except Exception:
        ret['status'] = 1
    return ret


@app.post("/srl")
def srl(item: Item):  # 语义角色标注
    ret = {
        'status': 0,
        'texts': item.texts,
        'seg': [],
        'srl': [],
    }
    try:
        seg, hidden = ltp.seg(item.texts)
        res = ltp.srl(hidden)
        ret['seg'] = seg
        ret['srl'] = res
    except Exception:
        ret['status'] = 1
    return ret


@app.post("/dep")
def dep(item: Item):  # 依存句法分析
    ret = {
        'status': 0,
        'texts': item.texts,
        'seg': [],
        'dep': [],
    }
    try:
        seg, hidden = ltp.seg(item.texts)
        res = ltp.dep(hidden)
        ret['seg'] = seg
        ret['dep'] = res
    except Exception:
        ret['status'] = 1
    return ret


@app.post("/sdp")
def sdp(item: Item):  # 语义依存分析（树）
    ret = {
        'status': 0,
        'texts': item.texts,
        'seg': [],
        'sdp': [],
    }
    try:
        seg, hidden = ltp.seg(item.texts)
        res = ltp.sdp(hidden)
        ret['seg'] = seg
        ret['sdp'] = res
    except Exception:
        ret['status'] = 1
    return ret


@app.post("/sdpg")
def sdpg(item: Item):  # 语义依存分析（图）
    ret = {
        'status': 0,
        'texts': item.texts,
        'seg': [],
        'sdpg': [],
    }
    try:
        seg, hidden = ltp.seg(item.texts)
        res = ltp.sdp(hidden)
        ret['seg'] = seg
        ret['sdpg'] = res
    except Exception:
        ret['status'] = 1
    return ret


if __name__ == '__main__':
    uvicorn.run("test:app", reload=True)
