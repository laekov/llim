# -*- coding:utf-8 -*-
import pickle
d = []
with open('../../problem/test.txt', 'r', encoding = 'utf-8') as f:
    lines = f.read().split('\n')
    len_lines = len(lines)
    for i in range(0, len_lines, 2):
        if i + 1 < len_lines and len(lines[i]) > 0:
            d.append({ 'pinyin': lines[i].lower(), 'text': lines[i + 1] })
print(str(len(d)) + ' test cases loaded')
with open('../data/test.pickle', 'wb') as f:
    pickle.dump(d, f)
print('written')


