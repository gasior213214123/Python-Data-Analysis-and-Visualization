# -*- coding: cp1250 -*-

import numpy as np
import matplotlib.pyplot as plt
import fastnumbers as fn
import math

def readfile(filedir):

    with open(filedir, "r") as f:
        prices = []
        hps = []
        lines1 = []
        lines2 = []

        for line in f:
            line = line.split(',')

            hp = fn.fast_float(line[21], default=0)
            price = fn.fast_float(line[25], default=0)

            if fn.isfloat(hp):
                if hp > 20 and hp < 300:
                    hps.append(hp)
                else:
                    lines1.append(line)
            else:
                lines1.append(line)

            if fn.isfloat(price):
                if price > 1 and price < 60:
                    prices.append(price)
                else:
                    lines2.append(line)
            else:
                lines2.append(line)

    avghp = sum(hps) / len(hps)
    avgprice = sum(prices) / len(prices)

    for line in lines1:
        hp = avghp
        price = fn.fast_float(line[21])

        hps.append(hp)
        prices.append(price)

    for line in lines2:
        hp = fn.fast_float(line[25])
        price = avgprice

        hps.append(hp)
        prices.append(price)

    sort = zip(prices, hps)
    sort.sort()
    prices = [x for x, y in sort]
    hps = [y for x, y in sort]

    return prices , hps

def linregress(x, y):

    zipped = zip(x, y)

    n = float(len(x))
    sumx = float(sum(x))
    sumy = float(sum(y))
    sumx2 = float(sum([i * i for i in x]))
    sumxy = float(sum([i * j for i, j in zipped]))

    a = (n * sumxy - sumx * sumy) / (n * sumx2 - sumx * sumx)
    b = (sumy - a * sumx) / n

    X = x
    Y = [a * i + b for i in X]

    return a, b, X, Y

def calcdatums(x, y, Q1, Q3):

    IRQ = Q3 - Q1
    zipped = zip(x, y)
    datums = []

    for i in zipped:
        x, y = i
        if y < Q1 - 1.5 * IRQ or y > Q3 + 1.5 * IRQ:
                   datums.append(i)

    return datums

def analyze(data):

    def min1(data):
        x=1000.0
        for i in data:
            inum = float(i)
            if inum < x:
                x = inum
        return x

    def max1(data):
        x=0
        for i in data:
            inum = float(i)
            if inum > x:
                x = inum
        return x

    def median1(data):
        n = len(data)
        if n % 2 == 1:
            return sorted(data)[n//2]
        else:
            return sum(sorted(data)[n//2-1:n//2+1])/2.0

    def mean1(data):
        n = len(data)
        x = sum(data)
        avg = x / n
        return avg

    def stddev(data):
        mean = float(sum(data)) / len(data)
        return math.sqrt(float(reduce(lambda x, y: x + y, map(lambda x: (x - mean) ** 2, data))) / len(data))

    def quartile1(data):
        return sorted(data)[int(len(data) * .25)]
    def quartile3(data):
        return sorted(data)[int(len(data) * .75)]

    minval = min1(data)
    maxval = max1(data)
    median = round(median1(data), 2)
    mean = round(mean1(data), 2)
    std = round(stddev(data), 2)
    Q1 = quartile1(data)
    Q3 = quartile3(data)
    IQR = Q3 - Q1
    lngth = len(data)

    return [minval, maxval, median, mean, std, Q1, Q3, IQR, lngth]

def estimate(n, a, b):

    X = [np.random.randint(1, 60) for i in range(0, n)]
    Y = []

    for x in X:
        Y.append(a * x + b)

    return X, Y

def chart(prices, hps, X, Y, X2, Y2, datums):

    unzipped = zip(*datums)

    plt.figure(1)
    plt.plot(prices, hps, 'k.', X, Y, '-c', X2, Y2, 'g.', unzipped[0], unzipped[1], 'r.', linewidth=1.0)
    plt.legend(["Dane bazowe", "Linia regresji", "Dane estymowane", "Punkty oddalone"])
    plt.gca().set_xlim([0, 60])
    plt.gca().set_ylim([0, 330])
    plt.ylabel("Ilosc koni mechanicznych (hp)")
    plt.xlabel("Cena auta(tys.)")
    plt.title("Wykres")
    plt.savefig("fig1.png")

    """plt.figure(2)
    plt.boxplot([hps], vert=False, sym='r.')
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    plt.xlabel("Ilosc koni mechanicznych (hp)")
    plt.title(u"Wykres pudelkowy koni mechanicznych (hp)")
    plt.savefig("fig2.png")

    plt.figure(3)
    plt.boxplot([prices], vert=False, sym='r.')
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    plt.xlabel("Cena auta(tys.")
    plt.title(u"Wykres pudelkowy ceny auta (tys.)")
    plt.savefig("fig3.png")"""

    plt.show()

def covariance(q, w):
    meanq = float(sum(q)) / len(q)
    meanw = float(sum(w)) / len(w)
    n = len(q)
    cov = sum([(x-meanq)*(y-meanw) for x, y in zip(q, w)]) / n
    return cov

if __name__ == "__main__":

    prices, hps = readfile("imports-85.txt")

    p = analyze(prices)
    h = analyze(hps)
    _a, b, X, Y = linregress(prices, hps)
    datums = calcdatums(prices, hps, h[5], h[6])
    X2, Y2 = estimate(10, _a, b)
    cov = covariance(prices, hps)
    pearson = round(cov / (p[4]*h[4]), 4)

    print "Ceny", prices
    print "Konie", hps
    print "Kowariancja", cov
    print "Prosta regresji liniowej : y = "+str(round(_a,2))+"x + "+str(round(b,2)), "\n"

    print "Dane: "
    print "#  ",\
        "{:>7}".format("Min"), "\t", \
            "{:>7}".format("Max"), "\t", \
            "{:>7}".format("Median"), "\t", \
            "{:>7}".format("Mean"), "\t", \
            "{:>7}".format("Std"), "\t", \
            "{:>7}".format("Q1"), "\t", \
            "{:>7}".format("Q3"), "\t", \
            "{:>7}".format("IQR"), "\t", \
            "{:>7}".format("Length"), "\t"
    print "Price:",\
        "{:7}".format(p[0]), "\t", \
            "{:7}".format(p[1]), "\t", \
            "{:7}".format(p[2]), "\t", \
            "{:7}".format(p[3]), "\t", \
            "{:7}".format(p[4]), "\t", \
            "{:7}".format(p[5]), "\t", \
            "{:7}".format(p[6]), "\t", \
            "{:7}".format(p[7]), "\t", \
            "{:7}".format(p[8]), "\t"
    print "HPS:", \
        "{:7}".format(h[0]), "\t", \
        "{:7}".format(h[1]), "\t", \
        "{:7}".format(h[2]), "\t", \
        "{:7}".format(h[3]), "\t", \
        "{:7}".format(h[4]), "\t", \
        "{:7}".format(h[5]), "\t", \
        "{:7}".format(h[6]), "\t", \
        "{:7}".format(h[7]), "\t", \
        "{:7}".format(h[8]), "\t"

    print "\nWspolczynnik korelacji liniowej Pearsona: ", pearson
    print "\nPunkty oddalone: ", datums
    print "\nDane estymowane: ", X2, Y2

    chart(prices, hps, X, Y, X2, Y2, datums)
