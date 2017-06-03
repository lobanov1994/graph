# -*- coding: utf-8 -*-
"""
Created on Sat Jun 03 02:59:13 2017

@author: xl47
"""

class heap:
    def __init__(self, A):
        self.A = A
        self.n = len(A)
        self.heapify()
        
    def remn(self, k0):
        k = k0
        while k < (self.n-1)/2:
            k1 = 2*k+1
            k2 = k1+1
            if k2 < self.n and self.A[k2] < self.A[k1]:
                k1 = k2
            if self.A[k] < self.A[k1]:
                break
            else:
                self.A[k],self.A[k1] = self.A[k1],self.A[k]
            k = k1
        if self.n == 2:
            if self.A[0] > self.A[1]:
                self.A[0],self.A[1] = self.A[1],self.A[0]
        
    def remv(self, k0):
        k = k0
        while k > 0:
            k1 = (k-1)/2
            if (self.A[k1] < self.A[k]):
                break
            else:
                self.A[k],self.A[k1] = self.A[k1],self.A[k]
            k = k1
    
    def getmin(self):
        min1 = self.A[0]
        self.A[0] = self.A[self.n-1]
        self.n += -1
        self.remn(0)
        return min1
    
    def add(self, a):
        self.A.append(a)
        self.n += 1
        self.remv(self.n-1)
        
    def remove(self, k0):
        a = self.A[k0]
        self.A[k0] = self.A[self.n-1]
        self.n += -1
        if self.A[k0] > a:
            self.remn(k0)
        else:
            self.remv[k0]

    def heapify(self):
        i = (self.n-1)/2
        while i >= 0:
            self.remn(i)
            i += -1
                        
def heapsort(A):
    h = heap(A)
    while h.n > 0:
        h.A[0],h.A[h.n-1] = h.A[h.n-1],A[0]
        h.n += -1
        h.remn(0)            
            

def heaptest():
    A = [4,62,32,76,34,65,125,72,56,3,6]
    h = heap(A)
    print h.A
    heapsort(A)
    print A      
            
heaptest()