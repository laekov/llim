# -*- coding:utf-8 -*-
import pickle

n = 687

mpd = { 'fw': {}, 'bw': {} }

def add2sglmp(i, a, b):
    global mpd
    if not a in mpd[i]:
        mpd[i][a] = { 'count': 0 }
    mpd[i][a]['count'] += 1
    if not b in mpd[i][a]:
        mpd[i][a][b] = 1
    else:
        mpd[i][a][b] += 1

def add2mp(a, b):
    add2sglmp('fw', a, b)
    add2sglmp('bw', b, a)

def add3mp(a, b, c):
    add2sglmp('fw', a + b, b)
    add2sglmp('bw', c + b, a)

for i in range(n + 1):
    with open('../data/data%03d.pickle' % i, 'rb') as f:
        wd = pickle.load(f)
        for s in wd:
            add2mp('<start>', s[0])
            add2mp(s[-1], '<end>')
            for j in range(len(s) - 1):
                add2mp(s[j], s[j + 1])
            for j in range(len(s) - 2):
                add3mp(s[j], s[j + 1], s[j + 2])
    if i % 16 == 0:
        print('data %d done' % i)

def clearMap3(d):
    rmi = []
    for i in mpd[d]:
        if len(i) == 2:
            sp = 0
            for j in mpd[d][i]:
                sp += mpd[d][i][j]
            rmlst = []
            for j in mpd[d][i]:
                if mpd[d][i][j] * 1000 < sp:
                    rmlst.append(j)
            if sp < 50:
                rmi.append(i)
            else:
                for j in rmlst:
                    del mpd[d][i][j]
    for i in rmi:
        del mpd[d][i]

print('Printing bare data')

with open('../data/map.pickle', 'wb') as f:
    pickle.dump(mpd, f)

print('Cleaning data')

clearMap3('fw')
clearMap3('bw')

print('Writing simplified data')
with open('../data/map_simple.pickle', 'wb') as f:
    pickle.dump(mpd, f)
