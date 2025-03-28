# ライブラリと関数と便利変数
# ライブラリ
from collections import deque, defaultdict, Counter
from math import pi
from itertools import permutations
import bisect
import sys

# cortedcontainersは使うときだけ wandbox非対応なので
# from sortedcontainers import SortedDict, SortedSet, SortedList


# 関数
def pow(x: int, n: int, t: int = 1):
    # O(log N)
    if t == 1:
        ans = 1
        while n:
            if n % 2:
                ans = ans * x
            x = x * x
            n >>= 1
        return ans
    ans = 1
    while n:
        if n % 2:
            ans = (ans * x) % t
        x = (x * x) % t
        n >>= 1
    return ans


def is_prime(n: int) -> bool:
    # O(√N)
    if n == 1:
        return False

    i = 2
    s = n**0.5

    while i < s:
        if n % i == 0:
            return False

        i += 1

    return True


def eratosthenes(n):
    primes = [True] * (n + 1)
    primes[0], primes[1] = False, False
    i = 2
    while i**2 <= n:
        if primes[i]:
            for k in range(i * 2, n + 1, i):
                primes[k] = False

        i += 1

    return [i for i, p in enumerate(primes) if p]


def gcd(a, b):
    while a > 0 and b > 0:
        if a > b:
            a = a % b
        else:
            b = b % a

    return max(a, b)


def lcm(a, b):
    return (a * b) // gcd(a, b)


# 標準入力系
def s():
    return sys.stdin.readline().rstrip()


def sl():
    return s().split()


def ii():
    return int(s())


def il(add_num: int = 0):
    return list(map(lambda i: int(i) + add_num, sl()))


# 便利変数
INF = 10**18
lowerlist = list("abcdefghijklmnopqrstuvwxyz")
upperlist = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")


# テンプレ
class SegmentTree:
    # 鉄則本のパクリですけどよろしく
    def __init__(self, N) -> None:
        # サイズは要素の数

        self.size = 1
        while self.size < N:
            self.size *= 2

        self.data = [0] * (self.size * 2)

    def update(self, ind, x):
        ind = ind + self.size - 1
        self.data[ind] = x

        while ind >= 2:
            ind //= 2
            self.data[ind] = max(self.data[ind * 2], self.data[ind * 2 + 1])

    def query(self, l, r, a, b, u):
        if r <= a or l >= b:
            return -INF
        if l <= a and b <= r:
            return self.data[u]

        m = (a + b) // 2
        return max(self.query(l, r, a, m, u * 2), self.query(l, r, m, b, u * 2 + 1))


# コード
N = ii()
S = s()
W = il()

# 子供の数を取っておく
CC = S.count("0")

# SとWをソートのため合わせる
L = [[S[i], W[i]] for i in range(N)]

# Lをソート
L.sort(key=lambda x: x[1])

# 答えを求める
ans = 0

# ラングレス圧縮するのでそのリスト
new = []

for i in range(N):
    # iが0の場合の処理
    if i == 0:
        if L[i][0] == "0":
            new.append([1, 0])
        else:
            new.append([0, 1])

        continue

    # iが0以外の場合
    if L[i - 1][1] == L[i][1]:
        # 前回の体重と同じ場合
        if L[i][0] == "0":
            new[-1][0] += 1
        else:
            new[-1][1] += 1
    else:
        # 前回の体重と違う場合
        ans = max(ans, N - (CC - new[-1][0]) - new[-1][1])

        if L[i][0] == "0":
            new.append([new[-1][0] + 1, new[-1][1]])
        else:
            new.append([new[-1][0], new[-1][1] + 1])

# 最後のケースに対応
ans = max(ans, N - (CC - new[-1][0]) - new[-1][1])

print(ans)
