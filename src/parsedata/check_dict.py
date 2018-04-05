# -*- coding:utf-8 -*-
import pickle
with open('../data/dict.pickle', 'rb') as f:
    d = pickle.load(f)
with open('../data/map.pickle', 'rb') as f:
    mp = pickle.load(f)
print(d['lu'][1])
print(d['rui'][1])
print(d['wo'])
print(d['qu'])
print(mp['fw']['<start>']['我'])
print(mp['fw']['<start>']['握'])
print(mp['fw']['我是'])
