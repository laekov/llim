# -*- coding:utf-8 -*-
import math
eps = .000001
innocent = math.exp(eps)

def getLnkVal(a, b, pin, direct):
    # print('checking %s to %s as %s' % (a, b, pin))
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
    lnk_v *= math.log(23 + totl, 23)
    if len(a) == 2:
        lnk_v *= tri_wei 
    return lnk_v

def evaluateAns(py, ans):
    n = len(ans)
    s = []
    for i in range(0, n - 1):
        if i + 2 < n:
            s.append(getLnkVal(ans[i], ans[i + 1], py[i + 1], 'fw'))
            # print('%s -> %s fw %e' % (ans[i], ans[i + 1], getLnkVal(ans[i], ans[i + 1], py[i + 1], 'fw')))
        if i + 3 < n:
            s.append(getLnkVal(ans[i] + ans[i + 1], ans[i + 2], py[i + 2], 'fw'))
        if i > 0:
            s.append(getLnkVal(ans[i + 1], ans[i], py[i], 'bw'))
        if i > 0 and i + 2 < n:
            s.append(getLnkVal(ans[i + 2] + ans[i + 1], ans[i], py[i], 'bw'))
            # print('%s <- %s fw %e' % (ans[i], ans[i + 1], getLnkVal(ans[i + 1], ans[i], py[i], 'bw')))
    s.sort(reverse = True)
    pi = 1.
    for i in range(max(1, min(len(s), int(len(s) * 0.7)))):
        pi *= s[i]
    return pi 
