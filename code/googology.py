from matches import RoundRobin

def inputContestants():
    out = []
    while True:
        print "Please input the name of the contestant or 'qq' to finish:"
        nxt = raw_input()
        if nxt:
            if nxt[:2] != "qq":
                out.append( nxt )
            else:
                return out
        
# Input contestants
contestants = inputContestants()

# Set up round robin


R = RoundRobin(contestants)
R.schedule()

# Play a round
results = []

while R.unplayed():
    R.playRound()

    # Pagerank the contestants
    R.rankTeams()

    R.showRankings()


    
