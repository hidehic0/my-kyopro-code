import random
from types import NoneType


def select(n: int | NoneType = None):
    if n is None:
        n = int(input("いくつ選びますか: "))

    L = set()

    for _ in [0] * n:
        rn = random.randrange(200, 370)

        while rn in L or rn == 316:
            rn = random.randrange(200, 370)

        L.add(rn)

    return [f"ABC{ind}" for ind in L]


if __name__ == "__main__":
    for contest_name in select(int(input("いくつ選びますか: "))):
        print(contest_name)
