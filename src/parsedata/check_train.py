# -*- coding:utf-8 -*-
import pickle
with open('../data/data012.pickle', 'rb') as f:
    d = pickle.load(f)
for i in d:
    print(i)
