# -*- coding:utf-8 -*-
import pickle
d = dict()
with open('../../problem/拼音汉字表.txt', 'r') as f:
    lines = f.read().decode('gbk').encode('utf-8').split('\r\n')
    for i in lines:
        l = i.split(' ') 
        d[l[0]] = l
print(str(len(d)) + ' pinyin loaded')
with open('../data/dict.pickle', 'wb') as f:
    pickle.dump(d, f)
print('written')


