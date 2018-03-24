# -*- coding:utf-8 -*-
import pickle
with open('../data/dict.pickle', 'rb') as f:
    d = pickle.load(f)
print(d['lu'][1])
print(d['rui'][1])
