# -*- coding: utf-8 -*-
"""
Created on Sat Mar 04 23:06:42 2017
Сделать:
@author: M.Lobanov
"""
class Bucket:
    def __init__(self, n, m):
        import numpy as np
        self.B = np.full(m, -1, dtype = 'int8')
        self.Fw = np.full(n, -1, dtype = 'int8')
        self.Bk = np.full(n, -1, dtype = 'int8')
    
    def get(self, k):
        i = self.B[k]
        if i != -1:
            self.B[k] = self.Fw[i]
        return i
    
    def insert(self, i, k):
        j = self.B[k]
        self.Fw[i] = j
        if j != -1:
            self.Bk[j] = i
        self.B[k] = i
    
    def remove(self, i, k):
        fi = self.Fw[i]
        bi = self.Bk[i]
        if i == self.B[k]:
            self.B[k] = fi
        else:
            self.Fw[bi] = fi
            if fi != -1:
                self.Bk[fi] = bi

def openGraph(filename):
    file = open(filename)
    s = file.read()
    file.close()
    a = []
    for i in s:
        if (i != " " and i != "\n"):
            a.append(int(i))
    j = 1
    x = []
    y = []
    weights = []
    countOfNodes = a[0]
    for i in range(len(a)//3):
        x.append(a[j])
        y.append(a[j+1])
        weights.append(a[j+2])
        j += 3
    return graph(countOfNodes, x, y, weights, 1)

class graph:
    def __init__(self, countOfNodes, x, y, weights, oriented):
        self.x = x
        self.y = y
        self.weights = weights
        self.h = []
        self.l = []
        self.maxWeight = 0
        self.countOfNodes = countOfNodes
        self.countOfRibs = len(x)
                
        for i in range(self.countOfNodes):
            self.h.append(-1)
            
        for i in range(self.countOfRibs):
            self.l.append(-1)
            if self.weights[i] > self.maxWeight:
                self.maxWeight = self.weights[i]
        
        if oriented:
        #Построение списка пучков дуг
            for k in range(self.countOfRibs):
                i = self.x[k]
                self.l[k] = self.h[i]
                self.h[i] = k
        else:
            self.makeNotOriented()
                  
    def add(self, i, j, weight):
        if self.__oriented:
            #Если дуги ранее не удалялись
            if self._deleted == -1:
                self.x.append(i)
                self.y.append(j)
                self.weights.append(weight)
                self.countOfRibs += 1
                #Добавление в список пучков дуг
                self.l.append(self.h[i])
                self.h[i] = len(self.l)-1
            #Если дуги удалялись ранее
            else:
                self.x[self._deleted] = i
                self.y[self._deleted] = j
                self.weights[self._deleted] = weight
                k = self.l[self._deleted]
                self.l[self._deleted] = self.h[i]
                self.h[i] = self._deleted
                self._deleted = k
                self.countOfRibs += 1
        #Для неориентированного графа:
        else:
            #Если граф пустой
            if len(self.xy) == 0:
                for b in xrange(1,5):
                    self.xy.append(-1)
                    self.l.append(b)
                    self.weights.append(-1)
                for b in range(6):
                    self.xy.append(-1)
                    self.l.append(-1)
                    self.weights.append(-1)
                self._capacity = len(self.xy)/2
                self._deleted = self.countOfRibs
            #Если в массиве нет места, его размер удваивается и перестраивается список пучков ребер
            elif self.countOfRibs == self._capacity:
                lastdel = len(self.xy) - 1
                for b in range(self.countOfRibs + 1):
                    self.xy.insert(self.countOfRibs,-1)
                    self.l.insert(self.countOfRibs,-1)
                    self.weights.insert(self.countOfRibs,-1)
                for b in range(self.countOfRibs - 1):
                    self.xy.insert(self.countOfRibs,-1)
                    self.weights.insert(self.countOfRibs,-1)
                    self.l.insert(self.countOfRibs,lastdel)
                    lastdel -= 1
                self._capacity = len(self.xy)/2
                self._deleted = self.countOfRibs
                self.createListOfRibBunches()
                
            whereInsert = self._deleted
            self.xy[whereInsert] = i
            self.xy[len(self.xy) - 1 - whereInsert] = j
            
            self.weights[whereInsert] = weight
            self.weights[len(self.xy) - 1 - whereInsert] = weight
            self._deleted = self.l[self._deleted]
            self.l[whereInsert] = self.h[i]
            self.l[len(self.l) - 1 - whereInsert] = self.h[j]
            self.h[i] = whereInsert
            self.h[j] = len(self.l) - 1 - whereInsert
            self.countOfRibs += 1
           
    def delete(self, i, j):
        if self.__oriented:
            prev = -1
            k = self.h[i]
            while (k != -1):
                if self.y[k] == j:
                    break
                prev = k
                k = self.l[k]
            if self.y[k] == j:
                if prev == -1:
                    self.h[i] = self.l[k]
                else:
                    self.l[prev] = self.l[k]
                self.l[k] = self._deleted
                self._deleted = k
        else:
            prev = -1
            k = self.h[i]
            delHappened = 0
            while k != -1:
                y = self.xy[len(self.xy) - k - 1]
                if y == j:
                    delHappened = 1
                    break
                prev = k
                k = self.l[k]
            if delHappened:    
                prev1 = -1
                k1 = self.h[j]
                while k1 != -1:
                    y = self.xy[len(self.xy) - k1 - 1]
                    if y == i:
                        break
                    prev1 = k1
                    k1 = self.l[k1]
                self.xy[k] = -1
                self.xy[k1] = -1
                #Удаляем из списка пучков ребер
                if prev != -1:
                    self.l[prev] = self.l[k]
                else:
                    self.h[i] = self.l[k]
                if prev1 != -1:
                    self.l[prev1] = self.l[k1]
                else:
                    self.h[j] = self.l[k1]
                #Добавление в список свободного места
                if k < k1:
                    self.l[k] = self._deleted
                    self._deleted = k
                    self.l[k1] = -1
                else:
                    self.l[k1] = self._deleted
                    self._deleted = k1
                    self.l[k] = -1
            
                self.countOfRibs -= 1
            
    def __str__(self):
        if self.__oriented:
            s = "digraph {\n"
            for i in range(len(self.h)):
                s += "\t" + str(i) + "\n"
            for i in range(len(self.h)):
                k = self.h[i]
                while k!=-1:
                    s += "\t\t" + str(self.x[k]) + " -> " + str(self.y[k]) + " [weight = " + str(self.weights[k]) + "]\n"
                    k = self.l[k]
            s += "}"
            return s
        else:
            s = "graph {\n"
            for i in range(self.countOfNodes):
                s += "\t" + str(i) + "\n"
            for k in range(self._capacity):
                if self.xy[k] != -1:
                    s += "\t\t" + str(self.xy[k]) 
                    s += " -- " + str(self.xy[len(self.xy) - 1 - k]) 
                    s += " [weight = " + str(self.weights[k]) + "]\n"
                    k = self.l[k]
            s += "}"
            return s
    def printAllRibs(self):
        if self.__oriented == 0:
            for i in range(self.countOfNodes):
                k = self.h[i]
                while k != -1:
                    x = self.xy[k]
                    y = self.xy[len(self.xy) - k -1]
                    print x, " -- ", y
                    k = self.l[k]
    
    def createPicture(self, filename = 'graph'):
        file = open(filename+".gv", "w")
        file.write(str(self))
        cmd = "dot -Tpng -O " + filename + ".gv"
        import subprocess
        subprocess.Popen(cmd, shell = True)
        cmd = filename + ".gv.png"
        subprocess.Popen(cmd, shell = True)
    
    #Возможно преобразование только из ориентированного графа в неориентированный
    def makeNotOriented(self):
        if self.__oriented:
            self._capacity = self.countOfRibs
            self.xy = []
            for i in range(len(self.x)):
                self.xy.append(self.x[i])
            for i in range(len(self.y)):
                self.xy.append(self.y[-1-i])
                self.weights.append(self.weights[-1-2*i])
            del(self.x)
            del(self.y)
            del(self.l)
            self.__oriented = bool(0)
            self.createListOfRibBunches()
     
        
    #Построение списка пучков ребер 
    def createListOfRibBunches(self):
        if self.__oriented == 0:
            self.h = []
            for i in range(self.countOfNodes):
                self.h.append(-1)
            self.l = []
            for i in self.xy:
                self.l.append(-1)
            for k in range(self._capacity):
                if self.xy[k] != -1:
                    i = self.xy[k]
                    #print "i = " + str(i) + "; k = " + str(k) + "; l[k] = " + str(self.h[i]) + "; h[i] = " + str(k)
                    self.l[k] = self.h[i]
                    self.h[i] = k
                    i = self.xy[len(self.xy) - 1 - k]
                    self.l[len(self.xy) - 1 - k] = self.h[i]
                    self.h[i] = len(self.xy) - 1 - k
            prevDel = -1
            for k in range(self._capacity):
                if self.xy[self._capacity - 1 - k] == -1:
                    self.l[self._capacity - 1 - k] = prevDel
                    prevDel = self._capacity - 1 - k
            self._deleted = prevDel
        
    def colouring(self):
        if self.__oriented == 0:
            self.colours = []
            s = []
            hn = []
            for i in range(self.countOfNodes):
                self.colours.append(-1)
                hn.append(self.h[i])
            #print self.colours
            #print hn
            colorNum = -1
            for i0 in range(self.countOfNodes):
                if self.colours[i0] == -1:
                    #print "Вершина " + str(i0) + " непокрашена, смотрим"
                    colorNum += 1
                    x = i0
                    while 1:
                        self.colours[x] = colorNum
                        j = hn[x]
                        while j != -1:
                            y = self.xy[len(self.xy) - 1 - j]
                            if self.colours[y] == -1:
                                #print "Вершина " + str(y) + " непокрашена, делаем шаг вперед"
                                break
                            #else:
                                #print "Вершина " + str(y) + " уже покрашена, смотрим следующую"
                            j = self.l[j]
                            #print j
                        if j != -1 :
                            hn[x] = self.l[j]
                            s.append(x)
                            x = y
                        else:
                            if (len(s) == 0):
                                break
                            else:
                                x = s.pop()
            print self.colours
                            
    def printIncedentNodes(self, i):
        k = self.h[i]
        print "Вершины, инцедентные с ",i,":"
        while k != -1:
            print "k = " + str(k) + "; Вершина: " + str(self.xy[len(self.xy) - 1 - k])
            k = self.l[k]
            
    def sort(self):
        if self.__oriented == 0:
            for i in range(len(self.xy)//2):
                for j in xrange(i + 1, len(self.xy)//2):
                    if self.weights[j] < self.weights[i]:
                        self.weights[j],self.weights[i] = self.weights[i],self.weights[j]
                        self.weights[len(self.weights)-1-i],self.weights[len(self.weights)-1-j] = self.weights[len(self.weights)-1-j],self.weights[len(self.weights)-1-i]
                        self.xy[j],self.xy[i] = self.xy[i],self.xy[j]
                        self.xy[len(self.xy) - 1 - j],self.xy[len(self.xy) - 1 - i] = self.xy[len(self.xy) - 1 - i],self.xy[len(self.xy) - 1 - j]
            self.createListOfRibBunches()
        
    def kruskul(self, subGraph):
        if self.__oriented == 0:
            def find(x):
                return colourOfNode[x]
            
            def union(mi, mj):
                if (countOfColours[mi] < countOfColours[mj]):
                    k = mi
                    l = mj
                else:
                    k = mj
                    l = mi
                i = firstNodeInSubMap[k]
                while (listOfNodesInSubMap[i] != -1):
                    colourOfNode[i] = l
                    i = listOfNodesInSubMap[i]
                colourOfNode[i] = l
                listOfNodesInSubMap[i] = firstNodeInSubMap[l]
                firstNodeInSubMap[l] = firstNodeInSubMap[k]
                countOfColours[l] += countOfColours[k]
            self.colouring()
            self.sort()
            countOfNodesInSubGraph = 0      #Имеется ввиду количество вершин в компоненте связности, для которой запускается алгоритм Краскала 
            for i in self.colours:
                if i == subGraph:
                    countOfNodesInSubGraph += 1
            #print "[Kruskul] Кол-во ребер, которые нужно соединить = " + str(countOfNodesInSubGraph)
            colourOfNode = []
            countOfColoredNodes = 1
            choosenRibs = []
            firstNodeInSubMap = []
            listOfNodesInSubMap = []
            countOfColours = []
            for i in range(self.countOfNodes):
                colourOfNode.append(i)
                firstNodeInSubMap.append(i)
                listOfNodesInSubMap.append(-1)
                countOfColours.append(1)
            k = 0
            while k < self._capacity and countOfColoredNodes < countOfNodesInSubGraph :
                #print "[Kruskul] k = " + str(k)
                #print "[Kruskul] " + str(colourOfNode)
                #print self.xy
                if self.xy[k] != -1:
                    x = self.xy[k]
                    y = self.xy[len(self.xy)-1-k]
                    if self.colours[x] == subGraph and self.colours[y] == subGraph:
                        mx = find(x)
                        my = find(y)
                        #print "[Kruskul] x = " + str(x) + "; y = " + str(y) + "; mx = " + str(mx) + "; my = " + str(my)
                        if mx != my:
                            choosenRibs.append(k)
                            countOfColoredNodes += 1
                            union(mx, my)
                    k += 1
            n1 = self.countOfNodes
            x1 = []
            y1 = []
            w1 = []
            for i in choosenRibs:
                x1.append(self.xy[i])
                y1.append(self.xy[len(self.xy)-1-i])
                w1.append(self.weights[i])
            return graph(n1, x1, y1, w1, 0)                  
        
    def BFS(self, s):
        if self.__oriented:
            self.r = []
            self.p = []
            for i in range(self.countOfNodes):
                self.r.append(self.countOfNodes)
                self.p.append(-2)
            q = []
            
            self.r[s] = 0
            self.p[s] = -1
            q.append(s)
            while len(q) > 0:
                x1 = q.pop(0)
                k = self.h[x1]
                while k != -1:
                    y1 = self.y[k]
                    if self.r[y1] == self.countOfNodes:
                        self.r[y1] = self.r[x1] + 1
                        self.p[y1] = k
                        q.append(y1)
                    k = self.l[k]
            s1 = ''
            s2 = ''
            for i in range(self.countOfNodes):
                if self.p[i] != -1:
                    s1 = str(i)
                    x1 = self.x[self.p[i]]
                    while x1 != s:
                        s1 = str(x1) + ' --> ' + s1
                        x1 = self.x[self.p[x1]]
                    s1 = str(s) + ' --> ' + s1
                    s2 = s2 + s1 + "\n"
            return s2
        
    def dijkstra(self, s):
        if self.__oriented:
            self.r = []
            self.p = []
            inf = 1000000
            for i in range(self.countOfNodes):
                self.r.append(inf)
                self.p.append(-2)
            m1 = self.countOfNodes * self.maxWeight
            bucket = Bucket(self.countOfNodes, m1)
            bucket.insert(s, 0)
            self.r[s]=0
            self.p[s]=-1
            
            for b in range(m1):
                x1 = bucket.get(b)
                while x1 != -1:
                    k = self.h[x1]
                    while k != -1:
                        y1 = self.y[k]
                        ry1 = self.r[y1]
                        if self.r[x1] + self.weights[k] < ry1:
                            self.r[y1] = self.r[x1] + self.weights[k]
                            self.p[y1] = k
                            if ry1 != inf:
                                bucket.remove(y1, ry1)
                            bucket.insert(y1, self.r[y1])
                        k = self.l[k]
                    x1=bucket.get(b)
            print self.r,self.p
            s1 = ''
            s2 = ''
            for i in range(self.countOfNodes):
                if self.p[i] != -1:
                    s1 = str(i)
                    x1 = self.x[self.p[i]]
                    k=0
                    while x1 != s and k<10:
                        s1 = str(x1) + ' --> ' + s1
                        x1 = self.x[self.p[x1]]
                        k += 1
                    s1 = str(s) + ' --> ' + s1
                    s2 = s2 + s1 + "\n"
            return s2
                
        
        
    countOfNodes = 0
    _deleted = -1
    __oriented = True

# %% Cell 2
def testAddDel():
    gr = openGraph("graphs/graph2.txt")
    for i in range(len(gr.x)):    
        gr.delete(gr.x[i], gr.y[i])
    gr.add(3,2,4)
    gr.add(0,1,2)
    gr.add(0,2,3)
    gr.add(1,2,1)
    gr.add(2,3,3)
    gr.add(3,4,2)
    gr.add(3,0,1)
    gr.add(3,1,2)
    gr.add(4,2,4)
    gr.add(4,1,5)
    print gr
    print zip(gr.x,gr.y)
    print gr.h
    print gr.l
    print gr._deleted
    gr.createPicture("graphs/graph2")

def testKruskul():
    gr = openGraph("graphs/graph4.txt")
    gr.makeNotOriented()
    print gr
    gr.sort()
    print gr
    gr.createPicture("graphs/graph4")
    gr1 = gr.kruskul(0)
    print gr1
    gr1.createPicture("graphs/graph4tree")
    
def testBFS():
    gr = openGraph("graphs/graph5.txt")
    print gr
    print gr.BFS(0)
    print gr.r
    print gr.p
    
def testDijkstra():
    gr = openGraph("graphs/graph6.txt")
    print gr
    print gr.dijkstra(0)
    
def testAddDelNotOriented1():
    gr = openGraph("graphs/graph6.txt")
    gr.makeNotOriented()
    gr.printAllRibs()
    print gr
    print len(gr.xy), gr.xy
    gr.add(3,2,10)
    print len(gr.xy), gr.xy
    print gr
    gr.createPicture("graphs/graph6afteradd")
    
def testAddDelNotOriented2():
    gr = graph(9, [], [], [], 0)
    gr.delete(0,1)
    gr.add(0,1,1)
    gr.printAllRibs()
    print "\n"
    gr.delete(0,1)
    gr.add(0,3,1)
    gr.delete(0,2)
    gr.add(0,2,1)
    gr.add(1,2,2)
    gr.add(1,3,3)
    gr.add(4,5,1)
    gr.printAllRibs()
    print "\n"
    gr.add(5,6,1)
    gr.add(6,7,2)
    gr.printAllRibs()
    print len(gr.l), gr.l
    print gr.xy,gr.h,gr.l,gr._deleted
    print gr
    gr.delete(3,0)
    print gr
    
testAddDelNotOriented1()
