from collections import defaultdict
from random import random
from math import sin, cos
A, B, C, D, T = 0, 1, 2, 3, 4

results =(A,B), (A,D), (B,C), (B,D), (C,A), (C,D), (T,A), (B,T), (C,T), (D,T)

class Vector:
    def __init__(self, l):
        self.elements = l
        self.size = len(l)
    def __getitem__(self, i):
        return self.elements[i]
    def __len__(self):
        return self.size
    def __sub__(self, other):
        return Vector( map( lambda i: i[0] - i[1], zip(self.elements, other.elements)))
    def __add__(self, other):
        return Vector( map( lambda i: i[0] + i[1], zip(self.elements, other.elements)))

    def __rmul__(self, k):
        return Vector( map( lambda i: i*k, self.elements))
    
    def dot(self, other):
        return sum( map (lambda i: i[0]*i[1], zip(self.elements, other.elements)))
    def __repr__(self):
        return "%r" % self.elements
    
class Matrix:
    def __init__(self, d):
        self.elements = d
        m = [max(i) for i in d]
        self.size = max(m)+1
        
    def get(self, i , j):
        if (i,j) in self.elements:
            return  self.elements[(i,j)]
        else:
            return 0.

    def prm(self, p =0.85):
        out = {}
        for i in range(self.size):
            for j in range(self.size):
                out[(i,j)] = self.get(i,j) * p + (1-p)/self.size - (1 if i==j else 0)
        return Matrix(out)

    def mul(self, vec):
        out = []
        for i in range(self.size):
            V = Vector( [self.get(i, j) for j in range(self.size) ])
            out.append(V.dot(vec))
        return Vector(out)
    
    def __repr__(self):
        out = ""
        for i in range(self.size):
            for j in range(self.size):
                next = "%10.2f\t" % (self.get(j,i))
                out += next
            out += "\n"
        return out
        

        
def matrixFromResults(res):
    # set the results by loser
    cols = defaultdict(set)
    out = {}
    for r in res:
        cols[r[1]].add(r[0])
    for L in cols:
        s = cols[L]
        ni = 1./len(s)
        for W in s:
            out[(L, W)] = ni
    out = Matrix(out)
    return out

def thetaToX(t):
    x = [cos(t[0])]
    for i in range(1,len(t)):
        x.append( x[i-1] * sin(t[i-1]) * cos(t[i]) / cos(t[i-1]) )
    return Vector(x)

def pagerank(M, t = None):
    # we want X such that (M-I).X = 0 
    # let Z = [(M-I).X]^2
    # let D = [(M-I).(X+e)]^2 - Z 
    # let E = (-Z / |D|^2 ) D
    # let X* = X + E
    n = M.size
    if t is None:
        t = Vector([random() for i in range(n)])
    x = thetaToX(t)
    Z = M.mul(x)
    ZZ = Z.dot(Z)

    t1 = Vector([ti + 0.0001 for ti in t])
    x1 = thetaToX(t1)
    D0 = M.mul(x1)
    D = D0 - Z

    E = (-ZZ / t.dot(t) ) * t
    print E.dot(E)
    if E.dot(E) > 0.1:
        E = (0.1/E.dot(E)) * E
    print ZZ
    
    return t+E, thetaToX(t+E)
    
        

M= matrixFromResults(results)
t = None
for i in range(10):
    t, x = pagerank(M.prm(), t= t)
    print ".. " , x
