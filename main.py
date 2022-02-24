#Adam Wieliczko

import math
import statistics

import matplotlib.pyplot as plt
import scipy.stats



def G(seed=5, fact = 17713, con = 11, div = 2147483647):
    #Generator liczb całkowitych o rozkładzie równomiernym

    if div == 0:
        result = (seed * fact + con) % 2147483647
    else:
        result = (seed * fact + con) % div
    return result



def J(seed=5, fact = 17713, con = 11, div = 2147483647):
    #Generator liczb w przedziale (0,1) o rozkładzie równomiernym

    result = 1 + G(seed, fact, con, div)

    if div != 0:
        result = result / (div + 1)
    else:
        result = result / 2147483648
    return result


def B(seed = 5, p = 0.5, fact = 17713, con = 11, div = 2147483647):
    #Generator liczb z rozkładu Bernoulliego (czyli albo, 1 albo 0)

    result = J(seed, fact, con, div)

    if result >= p:
        result = 0
    else:
        result = 1

    return result


def D(seed = 5, p = 0.5, n = 10, fact = 17713, con = 11, div = 2147483647):
    #Generator liczb naturalnych o rozkładzie dwumianowym

    result = 0
    i = 1

    U = J(seed, fact, con, div)

    while i < n:
        if U <= p:
            U = U / p
            result = result + 1
        else:
            U = (1 - U)/(1 - p)

        i = i + 1
    return result

def P(seed = 5, lambd = 2, fact = 17713, con = 11, div = 2147483647):
    #Generator liczb naturalnych o rozkładzie Poissona

    result = 0
    S = 1
    q = math.exp((-1) * lambd)

    seedJ = seed

    while S > q:
        S = S * J(seedJ, fact, con, div)
        result = result + 1

        seedJ = G(seedJ, fact, con, div)

    return (result - 1)

def W(seed = 5, lambd = 3, fact = 17713, con = 11, div = 2147483647):
    #Generator liczb rzeczywistych (dodatnich) o rozkładzie wykładniczym
    result = (-1) * (math.log(J(seed, fact, con, div))) / lambd
    return result

def N(seed = 5, seedTwo = 5, factToN = 17, conToN = 11, fact = 17713, con = 11, div = 2147483647):
    #Generator liczb rzeczywistych o rozkładzie normalnym
    UOne = J(seed, fact, con, div)
    UTwo = J(seedTwo, fact + 2000, con + 2222, div)

    UOne = math.sqrt((-2) * math.log(UOne))
    UTwo = 2 * math.pi * UTwo
    return ((UOne * math.cos(UTwo)) * factToN + conToN)

def pointsGenerator(seed = 12):
    result = G(seed)
    result = result % 13

    return result


def SeriesTest(seed, n, whatGen):
    whatSeed = seed
    arr = []
    for i in range(0, n):
        if whatGen == 'G':
            arr.append(G(whatSeed))
        elif whatGen == 'J':
            arr.append(J(whatSeed))
        elif whatGen == 'D':
            arr.append(D(whatSeed))
        elif whatGen == 'W':
            arr.append(W(whatSeed))
        elif whatGen == 'N':
            arr.append(N(whatSeed))
        whatSeed = G(whatSeed)

    median = statistics.median(arr)

    newArr = []
    biggerNumbers = 0
    smallerNumbers = 0
    numbersOfSeries = 0

    for i in range(0, n):
        if arr[i] > median:
            newArr.append(1)
            biggerNumbers = biggerNumbers + 1
        elif arr[i] < median:
            newArr.append(0)
            smallerNumbers = smallerNumbers + 1

    for i in range(1, biggerNumbers + smallerNumbers):
        if newArr[i] != newArr[i - 1]:
            numbersOfSeries = numbersOfSeries + 1

    mean = 1 + (2 * biggerNumbers * smallerNumbers)/(biggerNumbers + smallerNumbers)
    variance = (2 * biggerNumbers * smallerNumbers) * (2 * biggerNumbers * smallerNumbers - (biggerNumbers + smallerNumbers))
    dividable = (((biggerNumbers + smallerNumbers) - 1) * (biggerNumbers + smallerNumbers) * (biggerNumbers + smallerNumbers))
    if dividable != 0:
        variance = variance / dividable

    Z = (numbersOfSeries - mean)/math.sqrt(variance)

    #odcinam 2,5% po każdej stronie w rozkładzie normalnym standaryzowanym

    if Z > -1.96 and Z < 1.96:
        print("Test udany")
    else:
        print("Test nieudany")



def MMVKtest(seed, n, whatGen=G, first=0, second=0):

    whatSeed = seed
    arr = []

    for i in range(0, n):
        if whatGen == 'G':
            arr.append(G(whatSeed, 17713, 11, first))
        elif whatGen == 'J':
            arr.append(J(whatSeed, 17713, 11, first))
        elif whatGen == 'B':
            arr.append(B(whatSeed, first))
        elif whatGen == 'D':
            arr.append(D(whatSeed, first, second))
        elif whatGen == 'P':
            arr.append(P(whatSeed, first))
        elif whatGen == 'W':
            arr.append(W(whatSeed, first))
        elif whatGen == 'N':
            arr.append(N(whatSeed, first, second))

        whatSeed = G(whatSeed, 17713, 11)

    mean = 0
    for i in range(0, n):
        mean = mean + arr[i]/n

    if whatGen != 'B':
        med = statistics.median(arr)
    var = statistics.variance(arr)
    kurt = scipy.stats.kurtosis(arr)

    print("Otrzymana wartość średnia:", mean)
    if whatGen != 'B':
        print("Otrzymana mediana:", med)
    print("Otrzymana wariancja:", var)
    print("Otrzymana kurtoza:", kurt)
    print()

    if whatGen == 'G':
        if first == 0:
            first = 2147483647

        print("Prawidłowa wartość średnia:", first/2)
        print("Prawidłowa mediana:", first/2)
        print("Prawidłowa wariancja:", first * first/12)
        print("Prawidłowa kurtozja:", -(6/5))
    elif whatGen == 'J':
        print("Prawidłowa wartość średnia:", 0.5)
        print("Prawidłowa mediana:", 0.5)
        print("Prawidłowa wariancja:", 1/12)
        print("Prawidłowa kurtozja:", -(6/5))
    elif whatGen == 'B':
        print("Prawidłowa wartość średnia:", first)
        print("Prawidłowa wariancja:", first * (1 - first))
        print("Prawidłowa kurtozja:", (6 * first * first - 6 * first + 1)/(first * (1 - first)))
    elif whatGen == 'D':
        print("Prawidłowa wartość średnia:", first * second)
        print("Prawidłowa mediana:", math.floor(first * second), "bądź wartość mniejsza lub większa o 1")
        vari = (first*second*(1 - first))
        print("Prawidłowa wariancja:", vari)
        print("Prawidłowa kurtozja:", ((1 - 6 * first * (1 - first))/vari))
    elif whatGen == 'P':
        print("Prawidłowa wartość średnia:", first)
        print("Prawidłowa mediana:", math.floor(first + (1/3) + (0.02 / first)))
        print("Prawidłowa wariancja:", first)
        print("Prawidłowa kurtozja:", math.pow(first, -1))
    elif whatGen == 'W':
        print("Prawidłowa wartość średnia:", 1/first)
        print("Prawidłowa mediana:", math.log(2)/first)
        print("Prawidłowa wariancja:", 1/(first * first))
        print("Prawidłowa kurtozja:", 6)
    elif whatGen == 'N':
        print("Prawidłowa kurtozja:", -3)

    print()

"""
#PRZYKLADOWE WYNIKI + HISTOGRAMY

whatSeed = 100
arr = []
for i in range(0, 200000):
    arr.append(G(whatSeed))
    whatSeed = G(whatSeed)

plt.hist(arr)
plt.show()

whatSeed = 100
arr = []
for i in range(0, 200000):
    arr.append(J(whatSeed))
    whatSeed = G(whatSeed)

plt.hist(arr)
plt.show()

whatSeed = 100
arr = []
for i in range(0, 200000):
    arr.append(B(whatSeed))
    whatSeed = G(whatSeed)

plt.hist(arr)
plt.show()

whatSeed = 100
arr = []
for i in range(0, 200000):
    arr.append(D(whatSeed))
    whatSeed = G(whatSeed)

plt.hist(arr)
plt.show()

whatSeed = 100
arr = []
for i in range(0, 200000):
    arr.append(P(whatSeed))
    whatSeed = G(whatSeed)

plt.hist(arr)
plt.show()

whatSeed = 100
arr = []
for i in range(0, 200000):
    arr.append(W(whatSeed))
    whatSeed = G(whatSeed)

plt.hist(arr)
plt.show()

whatSeed = 100
arr = []
for i in range(0, 200000):
    arr.append(N(whatSeed))
    whatSeed = G(whatSeed)

plt.hist(arr)
plt.show()
"""

print(G(0.3, 6776, 341, 1))

#PRZYKLADOWE TESTY
"""
print("Testy generatora G")

SeriesTest(1, 10000, 'G')
SeriesTest(55, 200000, 'G')
SeriesTest(100, 200000, 'G')
SeriesTest(155, 200000, 'G')
SeriesTest(555, 200000, 'G')
SeriesTest(955, 200000, 'G')

print("Testy generatora J")

SeriesTest(1, 10000, 'J')
SeriesTest(55, 200000, 'J')
SeriesTest(100, 200000, 'J')
SeriesTest(155, 200000, 'J')
SeriesTest(555, 200000, 'J')
SeriesTest(955, 200000, 'J')

print("Testy generatora D")

SeriesTest(1, 10000, 'D')
SeriesTest(55, 200000, 'D')
SeriesTest(100, 200000, 'D')
SeriesTest(185, 200000, 'D')
SeriesTest(555, 200000, 'D')
SeriesTest(955, 200000, 'D')

print("Testy generatora W")

SeriesTest(1, 10000, 'W')
SeriesTest(55, 200000, 'W')
SeriesTest(100, 200000, 'W')
SeriesTest(155, 200000, 'W')
SeriesTest(555, 200000, 'W')
SeriesTest(955, 200000, 'W')

print("Testy generatora N")

SeriesTest(1, 10000, 'N')
SeriesTest(55, 200000, 'N')
SeriesTest(100, 200000, 'N')
SeriesTest(155, 200000, 'N')
SeriesTest(555, 200000, 'N')
SeriesTest(955, 200000, 'N')


print("Testy MMVK generatora G")

MMVKtest(245, 300000, 'G')
MMVKtest(260, 300000, 'G')
MMVKtest(245, 300000, 'G', 50000)

print("Testy MMVK generatora J")

MMVKtest(245, 300000, 'J')
MMVKtest(260, 300000, 'J')
MMVKtest(245, 300000, 'J', 50000)

print("Testy MMVK generatora B")

MMVKtest(2405, 300000, 'B', 0.4)
MMVKtest(2045, 300000, 'B', 0.6)
MMVKtest(2045, 300000, 'B', 0.2)

print("Testy MMVK generatora D")

MMVKtest(2405, 300000, 'D', 0.4, 100)
MMVKtest(2045, 300000, 'D', 0.6, 100)
MMVKtest(2045, 300000, 'D', 0.2, 100)

print("Testy MMVK generatora P")

MMVKtest(2405, 300000, 'P', 4)
MMVKtest(2045, 300000, 'P', 6)
MMVKtest(2045, 300000, 'P', 2)

print("Testy MMVK generatora W")

MMVKtest(2405, 300000, 'W', 4)
MMVKtest(2045, 300000, 'W', 6)
MMVKtest(2045, 300000, 'W', 2)

print("Testy MMVK generatora N")

MMVKtest(2405, 300000, 'N')
MMVKtest(2095, 300000, 'N', 33)
MMVKtest(2045, 300000, 'N', 587988)
"""