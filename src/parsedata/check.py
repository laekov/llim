# -*- coding:utf-8 -*-
import sys
in1 = sys.argv[1]
in2 = sys.argv[2]

with open(in1, 'r') as f1:
    d1 = f1.read().split('\n')
with open(in2, 'r') as f2:
    d2 = f2.read().split('\n')

n = min(len(d1), len(d2))

def strictCmp(a, b, p):
    s = 0.
    if len(a) != len(b) or len(a) < 1:
        return ( 0., 0., 0. )
    for i in range(len(a)):
        if a[i] == b[i]:
            s += 1.
    return (s, 1. if s == len(a) else 0., float(len(a)))

def rougeCmp(a, b, p):
    if len(a) != len(b) or len(a) < 1:
        return 0.
    a = '_' + a
    b = '_' + b
    n = len(a)
    f = []
    for i in range(n):
        f.append([ 0 ] * n)
    for i in range(1, n):
        for j in range(1, n):
            f[i][j] = max(f[i][j], f[i - 1][j], f[i][j - 1])
            if a[i] == b[j]:
                f[i][j] = max(f[i][j], f[i - 1][j - 1] + 1)
    n -= 1
    lcs = f[n][n]
    return 1. * lcs / max(n, 1.)

tot_len = 0.
acc_chr = 0.
rouge_l = 0.
acc_sent = 0.
sent_cnt = 0.

for i in range(n):
    x = d1[i].strip().rstrip()
    y = d2[i].strip().rstrip()
    if len(x) < 1:
        continue
    stres = strictCmp(x, y, 0)
    tot_len += stres[2]
    acc_chr += stres[0]
    rouge_l += rougeCmp(x, y, 0)
    acc_sent += stres[1]
    sent_cnt += 1.

print('Accuracy in sentence level: %.5f' % (acc_sent / sent_cnt))
print('Accuracy in char level: %.5f' % (acc_chr / tot_len))
print('Average ROUGE-L index: %.5f' % (rouge_l / sent_cnt))
