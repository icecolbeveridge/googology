# Given a list of n teams, create a round-robin schedule.
from collections import defaultdict
import numpy as np
from scipy import linalg

class Team:
    def __init__(self, name):
        self.name = name
        self.results = []
        self.score = -1.e30
    def __cmp__(self, other):
        return cmp(self.score, other.score)
    def __repr__(self):
        return "<Team: %s >" % self.name
    def __hash__(self):
        return hash(self.name)

    
toTeam = lambda t: Team(t) if type(t) == type("") else t

class Match:
    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2
    def play(self):
        if self.t1.name == "Bye":
            self.result = (self.t2, self.t1)
            return self.result
        elif self.t2.name == "Bye":
            self.result = (self.t1, self.t2)
            return self.result
        res = raw_input("Do you prefer (1) %r or (2) %r? " % (self.t1, self.t2))
        res = res.strip()
        if not res or res[0] not in "12":
            self.play()
        if res == "1":
            self.result = (self.t1, self.t2)
        else:
            self.result = (self.t2, self.t1)
        self.t1.results.append(self.result)
        self.t2.results.append(self.result)
        return self.result

    def getScore(self):
        return (self.t1.score - self.t2.score)**2
    

class MatchDay:
    def __init__(self):
        self.matches = []
        self.results = []
        self.score = None

    def addMatch(self, match):
        self.matches.append(match)
        
    def calcScore(self, force = False):
        if not force and self.score is not None:
            self.score = sum( [m.getScore() for m in matches])
        return self.score

    def playAll(self):
        for m in self.matches:
            self.results.append(m.play())
        return self.results
    
    def __cmp__(self,other):
        return cmp(self.score, other.score)
    
class RoundRobin:
    def __init__(self, teams):
        self.teams = map(toTeam, teams)
        self.n = len(teams)
        if self.n % 2 == 1:
            self.teams.append( Team("Bye") )
            self.n += 1
            self.hasBye = True
        else:
            self.hasBye = False
        self.matchdays = [ MatchDay() for i in range(self.n-1) ]
        self.matches = []
    def getRealTeams(self):
        return [t for t in self.teams if t.name != "Bye"]
        
    def teamNo(self, t):
        ts = self.getRealTeams()
        x = [i for i in range(len(ts)) if ts[i].name == t.name]
        if x:
            return x[0]
        else:
            return None
    
    def unplayed(self):
        return [w for w in self.matchdays if not w.results]
        
    def schedule(self):
        for i in range(self.n-1):
            for j in range(i, self.n-1):
                w = (i + j) % (self.n-1)
                if i != j:
                    self.matchdays[w].addMatch( Match(self.teams[i], self.teams[j] ) )
                else:
                    self.matchdays[w].addMatch( Match(self.teams[i], self.teams[-1]) )

    def playRound(self):
        u = self.unplayed()
        for w in u:
            w.calcScore(True)
        w = min(u)
        self.matches.extend(w.playAll())
        
        self.rankTeams()

    def rankTeams(self, df = 0.15):
        # set up a matrix
        n = len(self.teams) - (1 if self.hasBye else 0)
        cols = defaultdict(set)
        for r in self.matches: # each match is win team, lose team
            w, l = self.teamNo(r[0]), self.teamNo(r[1])
            if r[1].name != "Bye":
                cols[l].add(w)
                
        rows = [[0. for j in range(n)] for i in range(n)]
        for r in self.matches:
            w, l = self.teamNo(r[0]), self.teamNo(r[1])
            if r[1].name != "Bye":
                rows[w][l] = 1./len(cols[l])

        
        M = np.mat(rows)
        M = (df/n) * np.ones((n,n)) + (1-df) * M
        # normalise columns
        for i in range(n):
            M[:,i] /= sum(M[:,i])
        

        la, v = linalg.eig(M)


        best = (None, 0.)
        for i in range(len(la)):
            l = la[i]
            if abs(l) > abs(best[1]):
                best = [i, abs(l)]
        v = v[:, best[0]]
        
        ts = self.getRealTeams()
        for i in range(len(v)):
            ts[i].score = abs(v[i])
        self.teams.sort()

    def showRankings(self):
        ts = self.getRealTeams()
        ts.sort()
        ts.reverse()
        for t in ts:
            print "{0:20s} {1:5f}".format (t, t.score)
        
    def __repr__(self):
        out = ""
        for w, ms in enumerate(self.matchdays):
            out += "\nMatchday %d\n" % (w+1)
            for m in ms:
                if m[1] is not None:
                    out += "\t%s .vs. %s\n" % m
                else:
                    out += "\t(%s: bye)\n" % m[0]
        return out
                    
# T = ["Ansty", "Beaminster", "Charlton Marshall", "Dorchester", "Easton", "Fortuneswell", "Granby", "Hamworthy", "Iwerne"]
                
# R = RoundRobin(T)
# R.schedule()

# print R

                        
