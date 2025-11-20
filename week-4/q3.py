import numpy as np


def price(T, n, R, xj):
    return T - (T * n - R) * xj


R = T = 100
n = 3

avi, beni, gabi = range(3)
martef, shena, salon = range(3)
valuation = np.array(
    [
        [10, 20, 70],
        [20, 45, 35],
        [10, 45, 45],
    ]
)


edges = [0, 0.2, 0.4, 0.6, 0.8, 1]
prices = dict()
for p in edges:
    prices[p] = price(R=R, n=n, T=T, xj=p)

print(prices)

counter = 0
for a in edges:
    for b in edges:
        if a + b <= 1:
            counter += 1
            share = np.array([a, b, round(1 - a - b, 2)])
            print(share)
            timhur = tuple(prices[x] for x in share)
            timhur = np.array(timhur)
            print(timhur)
            vmt = valuation - timhur
            print(vmt)
            m = np.argmax(vmt, axis=1)
            print(m)
            print()

print("Total:", counter)


print(6 + 5 + 4 + 3 + 2 + 1)

t = np.array(
        [
            [0.4, 0.4, 0.2],
            [0.4, 0.2, 0.4],
            [0.6, 0.2, 0.2],
        ]
    ).mean(axis=0)
print(valuation - price(T, n, R, t))
print(np.argmax(valuation - price(T, n, R, xj=t), axis=1)
)
t = np.array([0.4, 0.3, .3])
print(valuation - price(T, n, R, t))
t = (np.array([0.5, 0.3, .2]) + np.array([.4, .3, .3])) / 2
print(valuation - price(T, n, R, t))
