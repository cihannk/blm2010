# Goksel AKTAS 170401033

import math
veriler = []
korelasyonlar = []


def fileOpen():
    with open("veriler.txt", 'r') as f:
        for line in f:
            veriler.append(int(line))


def fileWrite(results, katSayilar, first, last, derece, r):
    with open("sonuc.txt", 'a+') as f:
        f.write(str(first)+" - "+str(last-1) + ' araliklari icin ' +
                str(derece)+'. dereceden yaklasim\n')
        f.write('Korelasyon degeri= '+str(r)+"\n")
        f.write("Katsayilar= \t")

        for i in katSayilar:
            f.write(str(i)+"\t")


def gauss_jordan(m):
    size = len(m)
    for i in range(0, size):
        maxColumn = abs(m[i][i])
        maxrow = i
        for j in range(i + 1, size):
            if abs(m[j][i]) > maxColumn:
                maxColumn = abs(m[j][i])
                maxrow = j
        for k in range(i, size + 1):
            temp = m[maxrow][k]
            m[maxrow][k] = m[i][k]
            m[i][k] = temp

        for l in range(i + 1, size):
            c = -m[l][i] / m[i][i]
            for j in range(i, size + 1):
                if i == j:
                    m[l][j] = 0
                else:
                    m[l][j] += c * m[i][j]

    matris = [0 for i in range(size)]
    for i in range(size - 1, -1, -1):
        matris[i] = m[i][size] / m[i][i]
        for k in range(i - 1, -1, -1):
            m[k][size] -= m[k][i] * matris[i]
    return matris


def korelasyon(results, first, last):
    n = last - first
    yi = 0
    for i in range(first, last):
        yi += veriler[i]
    y_ussu = yi/n
    Sr = 0
    for i in range(first, last):
        Sr = (results[i-first] - veriler[i])**2 + Sr
    St = 0
    for i in range(first, last):
        St = St + (veriler[i] - y_ussu)**2
    r2 = abs((St-Sr)/St)
    r = math.sqrt(r2)
    return r


def veriHesap(first, last):
    dizi = []
    n = last - first
    for derece in range(1, 7):
        xVal = []
        for i in range(n):
            xVal.append(i+1)
        m = [[0 for i in range(derece+1)] for j in range(derece+1)]
        size = len(m)
        for i in range(size):
            for j in range(size):
                xSum = 0
                for k in range(n):
                    m[0][0] = len(xVal)
                    xSum = xVal[k]**(i+j) + xSum
                    m[i][j] = xSum

        xyResults = []
        for i in range(size):
            Sum = 0
            for j in range(first, last):
                Sum = Sum + (veriler[j]*(xVal[j-first]**i))
            xyResults.append(Sum)

        k = 0
        for i in m:
            i.append(xyResults[k])
            k = k+1

        katSayilar = gauss_jordan(m)

        results = []
        for i in range(n):
            toplam = 0
            for j in range(len(katSayilar)):
                toplam = toplam + katSayilar[j]*((i+1)**j)
                if j == derece:
                    results.append(int(toplam))
        r = korelasyon(results, first, last)
        dizi.append(r)
        fileWrite(results, katSayilar, first,
                  last, derece, r)

        best = 100
        index = 0
        for i in range(len(dizi)):
            temp = abs(1-dizi[i])
            if temp < best:
                best = temp
                index = i+1

        with open("sonuc.txt", 'a+') as f:
            f.write(""+str(first)+'-'+str(last-1) +
                    ' araliklarinda en iyi korelasyona sahip olan derece: '+str(index)+'\n')
            f.write('KORELASYON DEGERI:  '+str(dizi[index-1])+'\n')
            f.write('\n\n\n')


fileOpen()
veriHesap(0, len(veriler))
first, last = 0, 10

while(last < len(veriler)):
    veriHesap(first, last)
    first += 10
    last += 10
