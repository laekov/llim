# -*- coding:utf-8 -*-
import pickle
import sys
import math
from random import random, randint

with open('../data/map.pickle', 'rb') as fm:
    mp = pickle.load(fm)

with open('../data/dict.pickle', 'rb') as fd:
    dc = pickle.load(fd)

print('Initialized')
max_iter = 10
stable_iter = 5
eps = .000001
mul_co = 10.
innocent = math.exp(eps)

def getLnkVal(a, b, pin, direct):
    totl = 0
    for i in dc[pin]:
        if a in mp[direct] and i in mp[direct][a]:
            totl += mp[direct][a][i]
    if a in mp[direct] and b in mp[direct][a]:
        curl = mp[direct][a][b]
    else:
        curl = eps
    lnk_v = curl / (totl + 1)
    # if totl > 0:
        # lnk_v *= math.log(totl)
    lnk_v *= math.log(13 + totl, 13)
    return lnk_v

def evaluateAns(py, ans):
    n = len(ans)
    s = 1.
    for i in range(0, n - 1):
        if i + 2 < n:
            s *= getLnkVal(ans[i], ans[i + 1], py[i + 1], 'fw')
            # print('%s -> %s fw %e' % (ans[i], ans[i + 1], getLnkVal(ans[i], ans[i + 1], py[i + 1], 'fw')))
        if i > 0:
            s *= getLnkVal(ans[i + 1], ans[i], py[i], 'bw')
            # print('%s <- %s fw %e' % (ans[i], ans[i + 1], getLnkVal(ans[i + 1], ans[i], py[i], 'bw')))
    return s

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
    mul_x = math.log(p_cnt + math.e) / (totl + eps)
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
    chosen_p = random() * sum_p
    for i in wl:
        chosen_p -= wl[i]
        if chosen_p <= 0.:
            return i
    return '<err>'

def cmbAns(ans, plc = ''):
    return plc.join(ans[1 : -1])

def printAnsWithVal(py, ans):
    print('%s %e' % (cmbAns(ans), evaluateAns(py, ans)))

n_kep = 30

def pinyin2text(raw_line):
    a = [ '' ] + raw_line.strip().rstrip().split(' ') # For same id
    n = len(a) - 1
    ans = [ 'start' ] + [ '<todo>' ] * n + [ 'end' ]
    lrn_rat = 1
    for i in range(1, n + 1):
        ans[i] = randomFetchChar(ans[i - 1], a[i], 'fw', i == 1, ans[i], 0)
    best_ans = ans[:]
    best_ans_val = evaluateAns(a, ans)
    cur_val = best_ans_val
    max_rat = math.exp(10.)
    f = [ { 'start': { 'val': 1., 'text': 'start' } } ]
    for i in range(1, n + 1):
        f.append({})
        vals = []
        for v in dc[a[i]]:
            if v == a[i]:
                continue
            d = {
                    'val': 0.,
                    'text': v,
                    'from': '<unk>'
            }
            for jv in f[i - 1]:
                j = f[i - 1][jv]
                lnv = f[i - 1][jv]['val'] * getLnkVal(j['text'], v, a[i], 'fw')
                if i > 0:
                    lnv *= getLnkVal(v, j['text'], a[i - 1], 'bw')
                if i == n:
                    lnv *= getLnkVal('end', j['text'], a[i], 'bw')
                if lnv > d['val']:
                    d['val'] = lnv
                    d['from'] = j['text']
            f[i][v] = d
            vals.append(d['val'])
            vals.sort(reverse = True)
            if len(vals) > n_kep:
                vals = vals[0 : -1]
        mval = vals[-1]
        rmkeys = []
        for v in f[i]:
            if f[i][v]['val'] < mval:
                rmkeys.append(v)
        for k in rmkeys:
            del f[i][k]
    ans = [ '' ] * (n + 1)
    ls_val = 0.
    ls_txt = ''
    for jv in f[n]:
        if f[n][jv]['val'] > ls_val:
            ls_val = f[n][jv]['val']
            ls_txt = jv
    ans[n] = ls_txt
    for i in range(n - 1, 0, -1):
        ls_txt = f[i + 1][ls_txt]['from']
        ans[i] = ls_txt
    return ( ''.join(ans[1 : n + 1]), ans, evaluateAns(a, ans))

if __name__ == '__main__':
    while True:
        raw_line = sys.stdin.readline()
        if len(raw_line) < 1:
            break
        try:
            a = [ '' ] + raw_line.strip().rstrip().split(' ')
            ans = pinyin2text(raw_line)
            print('%s %e' % (ans[0], ans[2]))
        except Exception as err:
            print(err)
   
