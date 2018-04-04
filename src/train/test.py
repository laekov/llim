import pickle
import llpy

with open('../data/test.pickle', 'rb') as fd:
    test_cases = pickle.load(fd)

def strictCmp(a, b, p):
    return 1. if a == b else 0

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

def genResStr(tot, rat1, rat2):
    return 'Precision %.6f ROUGE-L %.6f' % ( 1. * rat1 / tot, 1. * rat2 / tot )

if __name__ == '__main__':
    tot = 0
    res_strict = 0
    res_lcs = 0
    for i in range(len(test_cases)):
        c = test_cases[i]
        ans = llpy.pinyin2text(c['pinyin'])
        tot += 1
        res_strict += strictCmp(ans, c['text'], c['pinyin'])
        res_lcs += rougeCmp(ans, c['text'], c['pinyin'])
        if i % 64 == 0:
            print('[Case 0 - %d] %s' % (i, genResStr(tot, res_strict, res_lcs)))

    print('[Fin] %s' % genResStr(tot, res_strict, res_lcs))
