# -*- coding:utf-8 -*-
import pickle
import json
import re

ctnt = []
cnt_data = 0
def logDownData():
    global ctnt
    global cnt_data
    with open('../data/data%03d.pickle' % cnt_data, 'wb') as f:
        pickle.dump(ctnt, f)
        print('data %d logged' % cnt_data)
    cnt_data += 1
    ctnt = []

def addSentences(s):
    ls = re.split(r' |,|\.|\d|，|。|！|？|“|”|《|》|：|；|、|\[|\]|（|）|[a-zA-Z]|/|:|;|!|…|\(|\)|%|\*|\^|\"|—|\-|【|】|●|@', s)
    for i in ls:
        if len(i) > 0:
            ctnt.append(i)
            if len(ctnt) >= 100000:
                logDownData()


def loadData():
    for i in range(1, 12):
        cnt_m = 0
        cnt_l = 0
        with open(('../../problem/sina_news/2016-%02d.txt' % i), 'r') as f:
            while True:
                l = f.readline()
                if len(l) == 0:
                    break
                d = json.loads(l)
                if 'html' in d:
                    addSentences(d['html'])
                if 'title' in d:
                    addSentences(d['title'])
        print('Month %d cnt %d' % (i, cnt_m))
    logDownData()

loadData()
# addSentences('讯（记者李芳 通讯员陈凌）昨天，86岁老人黄德望专程来到湖北工业大学，亲手在学校行政楼前的通告栏上贴上一封感谢信，感谢对他伸出援助之手')
