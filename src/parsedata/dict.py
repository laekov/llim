# -*- coding:utf-8 -*-
import pickle
d = dict()
with open('../../problem/拼音汉字表.txt', 'r', encoding = 'gbk') as f:
    lines = f.read().split('\n')
    for i in lines:
        l = i.split(' ') 
        d[l[0]] = l
d['qv'] = d['qu']
d['xv'] = d['xu']
d['jv'] = d['ju']
print(str(len(d)) + ' pinyin loaded')
with open('../data/dict.pickle', 'wb') as f:
    pickle.dump(d, f)
print('written')


