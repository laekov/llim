# -*- coding:utf-8 -*-
import pickle
with open('../data/test.pickle', 'rb') as f:
    tc = pickle.load(f)
print(tc[-1])
