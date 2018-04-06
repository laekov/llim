import pickle
import llpy
import matplotlib.pyplot as plt

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

ptx = []

def plotIt():
    n = len(ptx)
    y = []
    ptx.sort()
    for i in range(n):
        y.append(i / n)
    fig, ax = plt.subplots()
    plt.plot(ptx, y)
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    plt.savefig('fig.png')

def test(beg = 0, end = -1):
    if end == -1:
        end = len(test_cases)
    tot = 0
    res_strict = 0
    res_lcs = 0
    for i in range(beg, end):
        c = test_cases[i]
        r = llpy.pinyin2text(c['pinyin'])
        print('%s %e' % (r[0], r[2]))
        ans = r[0]
        tot += 1
        res_strict += strictCmp(ans, c['text'], c['pinyin'])
        res_lcs += rougeCmp(ans, c['text'], c['pinyin'])
        ptx.append(rougeCmp(ans, c['text'], c['pinyin']))
        if i % 16 == 0:
            plotIt()
            print('[Case 0 - %d] %s' % (i, genResStr(tot, res_strict, res_lcs)))

    print('[Fin] %s' % genResStr(tot, res_strict, res_lcs))

if __name__ == '__main__':
    test()
