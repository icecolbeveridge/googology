import numpy as np
from scipy import linalg
from collections import defaultdict
A, B, C, D, T = 0, 1, 2, 3, 4
N = 5
results =(A,B), (A,D), (B,C), (B,D), (C,A), (C,D), (T,A), (B,T), (C,T), (D,T)

M = np.zeros((N,N))
cols = defaultdict(set)
for r in results:
    cols[r[1]].add(r[0])

rows = [[0. for j in range(N)] for i in range(N)]
for r in results:
    rows[r[0]][r[1]] = 1./len(cols[r[1]])

M = np.mat( rows )
la, v = linalg.eig(M)

#which is closest to 1?

best = (None,  1e40)
for i in range(len(la)):
    l = la[i]
    if abs(l - 1) < abs(best[1]**2):
        best = [i, (l - 1)**2]

v = v[:, best[0]]
out = []
for i in range(len(v)):
    out.append( (-abs(v[i]), i) )

out.sort()
for i in out:
    print i
