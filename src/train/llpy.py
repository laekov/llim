# -*- coding:utf-8 -*-
import pickle
import sys
import math
from random import random

with open('../data/map.pickle', 'rb') as fm:
    mp = pickle.load(fm)

with open('../data/dict.pickle', 'rb') as fd:
    dc = pickle.load(fd)

print('Initialized')

max_iter = 100
stable_iter = 3
innocent = math.exp(.0000001)

def randomFetchChar(prv_chr, py, direct, is_head, last_ans, p_cnt):
    wl = {}
    if not py in dc:
        return '<unk>'
    sum_p = 0
    max_p = 0
    totl = 0
    for i in dc[py]:
        if prv_chr in mp[direct] and i in mp[direct][prv_chr]:
            totl += mp[direct][prv_chr][i]
    mul_x = 10. / (totl + .001)
    for i in dc[py]:
        if prv_chr in mp[direct] and i in mp[direct][prv_chr]:
            # print('%s = %.5f / %d * 10 (%.5lf)' % (i, mp[direct][prv_chr][i], totl, mul_x))
            wl[i] = math.exp(mp[direct][prv_chr][i] * mul_x)
        elif i != py:
            wl[i] = innocent
        else:
            continue
        max_p = max(wl[i], max_p)
        sum_p += wl[i]
    if last_ans != '<todo>':
        if not last_ans in wl:
            wl[last_ans] = innocent
        if is_head:
            p_prv = max_p * math.exp(p_cnt ** 2)
        else:
            p_prv = wl[last_ans] * math.exp(p_cnt)
        wl[last_ans] += p_prv
        sum_p += p_prv
    chosen_p = random() * sum_p
    for i in wl:
        chosen_p -= wl[i]
        if chosen_p <= 0.:
            return i
    return '<err>'

def pinyin2text(raw_line):
    a = [ '' ] + raw_line.strip().rstrip().split(' ') # For same id
    n = len(a) - 1
    ans = [ 'start' ] + [ '<todo>' ] * n + [ 'end' ]
    ctn_stable = 0
    for cnt_iter in range(0, max_iter):
        valid_iter = False
        for i in range(1, n + 1):
            g_chr = randomFetchChar(ans[i - 1], a[i], 'fw', i == 1, ans[i], ctn_stable)
            if g_chr != ans[i]:
                valid_iter = True
            ans[i] = g_chr
            #print('%s at %d %d' % (' '.join(ans[1 : n + 1]), cnt_iter, i))
        for i in range(n, 0, -1):
            g_chr = randomFetchChar(ans[i + 1], a[i], 'bw', i == n, ans[i], ctn_stable)
            if g_chr != ans[i]:
                valid_iter = True
            ans[i] = g_chr
            #print('%s at %d %d' % (' '.join(ans[1 : n + 1]), cnt_iter, i))
        if valid_iter:
            ctn_stable = 0
        else:
            ctn_stable += 1
            if ctn_stable >= stable_iter:
                break
        #print('%s at %d' % (' '.join(ans[1 : n + 1]), cnt_iter))
    return ''.join(ans[1 : n + 1])

if __name__ == '__main__':
    while True:
        raw_line = sys.stdin.readline()
        if len(raw_line) < 1:
            break
        print(pinyin2text(raw_line))
   
