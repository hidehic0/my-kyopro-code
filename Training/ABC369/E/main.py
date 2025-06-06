r"""
 ______________________
< it's hidehico's code >
 ----------------------
   \
    \
        .--.
       |o_o |
       |:_/ |
      //   \ \
     (|     | )
    /'\_   _/`\
    \___)=(___/
"""

# ライブラリと関数と便利変数
# ライブラリ
from collections import deque, defaultdict, Counter
from math import pi, gcd, lcm
from itertools import permutations
import bisect
import sys
import heapq
from typing import List, Any

# from atcoder.segtree import SegTree
# from atcoder.lazysegtree import LazySegTree
# from atcoder.dsu import DSU

# cortedcontainersは使うときだけ wandbox非対応なので
# from sortedcontainers import SortedDict, SortedSet, SortedList

# import pypyjit
# pypyjit.set_param("max_unroll_recursion=-1")

sys.setrecursionlimit(5 * 10**5)


# 関数
def is_prime(n):
    def f(a, t, n):
        x = pow(a, t, n)
        nt = n - 1
        while t != nt and x != 1 and x != nt:
            x = pow(x, 2, n)
            t <<= 1

        return t & 1 or x == nt

    if n == 2:
        return True
    elif n % 2 == 0:
        return False

    d = n - 1
    d >>= 1

    while d & 1 == 0:
        d >>= 1

    checklist = (
        [2, 7, 61] if 2**32 > n else [2, 325, 9375, 28178, 450775, 9780504, 1795265022]
    )

    for i in checklist:
        if i >= n:
            break
        if not f(i, d, n):
            return False

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


def calc_divisors(N):
    # 約数全列挙
    result = []

    for i in range(1, N + 1):
        if i * i > N:
            break

        if N % i != 0:
            continue

        heapq.heappush(result, i)
        if N // i != i:
            heapq.heappush(result, N // i)

    return result


def factorization(n):
    # 素因数分解
    result = []
    tmp = n
    for i in range(2, int(-(-(n**0.5) // 1)) + 1):
        if tmp % i == 0:
            cnt = 0
            while tmp % i == 0:
                cnt += 1
                tmp //= i
            result.append([i, cnt])

    if tmp != 1:
        result.append([tmp, 1])

    if result == []:
        result.append([n, 1])

    return result


def create_array2(a: int, b: int, default: Any = 0) -> List[List[Any]]:
    """
    ２次元配列を初期化する関数
    """
    return [[default] * b for _ in [0] * a]


def create_array3(a: int, b: int, c: int, default: Any = 0) -> List[List[List[Any]]]:
    """
    ３次元配列を初期化する関数
    """
    return [[[default] * c for _ in [0] * b] for _ in [0] * a]


# 標準入力系
# 一行に一つのstring
def s():
    return sys.stdin.readline().rstrip()


# 一行に複数のstring
def sl():
    return s().split()


# 一つのint
def ii():
    return int(s())


# 一行に複数のint
def il(add_num: int = 0):
    return list(map(lambda i: int(i) + add_num, sl()))


# 複数行の入力をサポート
def li(n: int, func, *args):
    return [func(*args) for _ in [0] * n]


# ac-library用メモ
"""
segtree

初期化するとき
Segtree(op,e,v)

opはマージする関数
例

def op(a,b):
    return a+b

eは初期化する値

vは配列の長さまたは、初期化する内容
"""


# 無向グラフ
class Graph:
    def __init__(self, N: int, dire: bool = False) -> None:
        self.N = N
        self.dire = dire
        self.grath = [[] for _ in [0] * self.N]
        self.in_deg = [0] * N

    def new_side(self, a: int, b: int):
        # 注意　0-indexedが前提
        self.grath[a].append(b)
        if self.dire:
            self.in_deg[b] += 1

        if not self.dire:
            self.grath[b].append(a)

    def side_input(self):
        # 新しい辺をinput
        a, b = il(-1)
        self.new_side(a, b)

    def input(self, M: int):
        # 複数行の辺のinput
        for _ in [0] * M:
            self.side_input()

    def get(self, a: int):
        # 頂点aの隣接点を出力
        return self.grath[a]

    def all(self):
        # グラフの内容をすべて出力
        return self.grath

    def topological(self, unique: bool = False):
        if not self.dire:
            raise ValueError("グラフが有向グラフでは有りません (╥﹏╥)")

        in_deg = self.in_deg[:]

        S: deque[int] = deque([])
        order: List[int] = []

        for i in range(self.N):
            if in_deg[i] == 0:
                S.append(i)

        while S:
            if unique and len(S) != 1:
                return [-1]

            cur = S.pop()
            order.append(cur)

            for nxt in self.get(cur):
                in_deg[nxt] -= 1

                if in_deg[nxt] == 0:
                    S.append(nxt)

        if sum(in_deg) > 0:
            return [-1]
        else:
            return [x for x in order]


# 重み付きグラフ
class GraphW:
    def __init__(self, N: int, dire: bool = False) -> None:
        self.N = N
        self.dire = dire
        self.grath = [[] for _ in [0] * self.N]

    def new_side(self, a: int, b: int, w: int):
        # 注意　0-indexedが前提
        self.grath[a].append((b, w))
        if not self.dire:
            self.grath[b].append((a, w))

    def side_input(self):
        # 新しい辺をinput
        a, b, w = il(-1)
        self.new_side(a, b, w)

    def input(self, M: int):
        # 複数行の辺のinput
        for _ in [0] * M:
            self.side_input()

    def get(self, a: int):
        # 頂点aの隣接点を出力
        return self.grath[a]

    def all(self):
        # グラフの内容をすべて出力
        return self.grath


# 便利変数
INF = 1 << 63
lowerlist = list("abcdefghijklmnopqrstuvwxyz")
upperlist = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")


# コード
N, M = il()
G = create_array2(N, N, INF)
L = []

for i in range(N):
    G[i][i] = 0

for _ in [0] * M:
    u, v, t = il()
    u -= 1
    v -= 1

    G[u][v] = min(G[u][v], t)
    G[v][u] = min(G[v][u], t)

    L.append((u, v, t))

Q = ii()

for k in range(N):
    for cur in range(N):
        for nxt in range(N):
            G[cur][nxt] = min(G[cur][nxt], G[cur][k] + G[k][nxt])


def solve():
    K = ii()
    B = il(-1)

    result = INF

    for p in permutations(B):
        for bit in range(1 << K):
            cur = 0
            ans = 0
            for i in range(K):
                if bit & (1 << i):
                    ans += G[cur][L[p[i]][0]] + L[p[i]][2]
                    cur = L[p[i]][1]
                else:
                    ans += G[cur][L[p[i]][1]] + L[p[i]][2]
                    cur = L[p[i]][0]

            ans += G[cur][N - 1]
            result = min(result, ans)

    return result


for _ in [0] * Q:
    print(solve())
