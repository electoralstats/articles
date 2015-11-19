#!/bin/python2
import csv
import Scraper

def findDII(margin):
    dii = (-11.0/24)*margin + (2411.0/24)
    return dii

#Get all the vote data from the Scraper script
rawActions = Scraper.getActions()
#First we find the data for all votes
actions = Scraper.filterActions(actions=rawActions, billsOnly=False, passedOnly=False)
margins = Scraper.getMargins(actions)
leg, votes = Scraper.getVoteDict(actions)
mccarthyID = "M001165"
mccarthyVotes = votes[mccarthyID]
repubs = {}
for l in leg:
    if leg[l]['Party'] == 'D':
        pass
    else:
        repubs[l] = leg[l]
        diisum = 0
        totalVotes = 0
        votesAgainst = 0
        for b in votes[l]:
            if votes[l][b] == 0:
                pass
            elif votes[l][b] != mccarthyVotes[b]:
                diisum += findDII(margins[b])
                votesAgainst += 1
                totalVotes += 1
            else:
                totalVotes += 1
        diiAvg = diisum/totalVotes if totalVotes else 0
        repubs[l]['NumberOfVotes'] = totalVotes
        repubs[l]['VotesAgainst'] = votesAgainst
        repubs[l]['DIISum'] = diisum
        repubs[l]['DIIAvg'] = diiAvg
outFile = open("DII_allvotes.csv", "wb")
output = csv.DictWriter(outFile, fieldnames=["Name", "NumberOfVotes", "VotesAgainst", "DIISum", "DIIAvg"], extrasaction='ignore')
output.writeheader()
for r in repubs:
    output.writerow(repubs[r])
outFile.close()

#We repeat the same process for just votes on billsOnlyactions = Scraper.filterActions(actions=rawActions, billsOnly=False, passedOnly=False)
actions = Scraper.filterActions(actions=rawActions, billsOnly=True, passedOnly=False)
margins = Scraper.getMargins(actions)
leg, votes = Scraper.getVoteDict(actions)
mccarthyID = "M001165"
mccarthyVotes = votes[mccarthyID]
repubs = {}
for l in leg:
    if leg[l]['Party'] == 'D':
        pass
    else:
        repubs[l] = leg[l]
        diisum = 0
        totalVotes = 0
        votesAgainst = 0
        for b in votes[l]:
            if votes[l][b] == 0:
                pass
            elif votes[l][b] != mccarthyVotes[b]:
                diisum += findDII(margins[b])
                votesAgainst += 1
                totalVotes += 1
            else:
                totalVotes += 1
        diiAvg = diisum/totalVotes if totalVotes else 0
        repubs[l]['NumberOfVotes'] = totalVotes
        repubs[l]['VotesAgainst'] = votesAgainst
        repubs[l]['DIISum'] = diisum
        repubs[l]['DIIAvg'] = diiAvg
outFile = open("DII_justbills.csv", "wb")
output = csv.DictWriter(outFile, fieldnames=["Name", "NumberOfVotes", "VotesAgainst", "DIISum", "DIIAvg"], extrasaction='ignore')
output.writeheader()
for r in repubs:
    output.writerow(repubs[r])
outFile.close()
