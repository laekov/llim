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
    lnk_v = (curl + eps) / (totl + eps)
    # if totl > 0:
        # lnk_v *= math.log(totl)
    lnk_v *= math.log(23 + totl, 23)
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
    while lrn_rat < max_rat:
        cnt_stable = 0
        if lrn_rat < 64:
            lrn_rat *= 1.1
        else:
            lrn_rat *= 1.7
        for cnt_iter in range(max_iter):
            b = ans[:]
            for p in range(1, n + 1):
                g_chr = randomFetchChar(b[p - 1], a[p], 'fw', p == 1, b[p], lrn_rat)
                prv_lnk_val = getLnkVal(b[p - 1], b[p], a[p], 'fw')
                cur_lnk_val = getLnkVal(b[p - 1], g_chr, a[p], 'fw')
                if cur_lnk_val > prv_lnk_val or random() * (prv_lnk_val / cur_lnk_val) < 1. / lrn_rat:
                    b[p] = g_chr
            for p in range(n, 0, -1):
                g_chr = randomFetchChar(ans[p + 1], a[p], 'bw', p == n, ans[p], lrn_rat)
                prv_lnk_val = getLnkVal(b[p + 1], b[p], a[p], 'bw')
                cur_lnk_val = getLnkVal(b[p + 1], g_chr, a[p], 'bw')
                if cur_lnk_val > prv_lnk_val or random() * (prv_lnk_val / cur_lnk_val) < 1. / lrn_rat:
                    b[p] = g_chr
            vb = evaluateAns(a, b)
            if vb > cur_val or random() * (cur_val / vb) < 1. / lrn_rat:
                cur_val = vb
                ans = b
                if cur_val > best_ans_val:
                    best_ans_val = cur_val
                    best_ans = ans[:]
                cnt_stable += 1
        if lrn_rat < 64:
            cur_val = best_ans_val
            ans = best_ans
        #print("%.5f %d" % (lrn_rat, cnt_stable))
        #printAnsWithVal(a, best_ans)
    #print('%s at %d' % (' '.join(ans[1 : n + 1]), cnt_iter))
    return ( ''.join(best_ans[1 : n + 1]), best_ans, best_ans_val)

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
   
