# -*- coding:utf-8 -*-
import pickle

n = 687

mpd = { 'fw': {}, 'bw': {} }

def add2mp(a, b):
    def add2sglmp(i, a, b):
        global mpd
        if not a in mpd[i]:
            mpd[i][a] = {}
        if not b in mpd[i][a]:
            mpd[i][a][b] = 1
        else:
            mpd[i][a][b] += 1
    add2sglmp('fw', a, b)
    add2sglmp('bw', b, a)

for i in range(n + 1):
    with open('../data/data%03d.pickle' % i, 'rb') as f:
        wd = pickle.load(f)
        for s in wd:
            add2mp('start', s[0])
            add2mp(s[-1], 'end')
            for j in range(len(s) - 1):
                add2mp(s[j], s[j + 1])
    if i % 16 == 0:
        print('data %d done' % i)

with open('../data/map.pickle', 'wb') as f:
    pickle.dump(mpd, f)
