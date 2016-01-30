#!/bin/python2
import csv
import Scraper
import json
import urllib2

mccarthyID = "M001165"
pelosiID = "P000197"

def findDII(margin):
    dii = (-11.0/24)*margin + (2411.0/24)
    return dii

#Get all the vote data from the Scraper script
rawActions = Scraper.getActions()
actionsAll = Scraper.filterActions(actions=rawActions, billsOnly=False, passedOnly=False)
marginsAll = Scraper.getMargins(actionsAll)
legAll, votesAll = Scraper.getVoteDict(actionsAll)
mccarthyVotes = votesAll[mccarthyID]
pelosiVotes = votesAll[pelosiID]

actionsBill = Scraper.filterActions(actions = rawActions, billsOnly = True, passedOnly = False)
marginsBill = Scraper.getMargins(actionsBill)
legBill, votesBill = Scraper.getVoteDict(actionsBill)

congress = {}
for l in legAll:
    if legAll[l]['Party'] == 'D':
        congress[l] = legAll[l]
        diiAllSum = 0
        totalAllVotes = 0
        votesAllAgainst = 0
        diiBillSum = 0
        totalBillVotes = 0
        votesBillAgainst = 0
        for b in votesAll[l]:
            if votesAll[l][b] == 0:
                pass
            elif votesAll[l][b] != pelosiVotes[b]:
                diiAllSum += findDII(marginsAll[b])
                votesAllAgainst += 1
                totalAllVotes += 1
            else:
                totalAllVotes += 1
        for b in votesBill[l]:
            if votesBill[l][b] == 0:
                pass
            elif votesBill[l][b] != pelosiVotes[b]:
                diiBillSum += findDII(marginsBill[b])
                votesBillAgainst += 1
                totalBillVotes += 1
            else:
                totalBillVotes += 1
        diiAllAvg = diiAllSum/totalAllVotes if totalAllVotes else 0
        diiBillAvg = diiBillSum/totalBillVotes if totalBillVotes else 0

    elif legAll[l]['Party'] == 'R':
        congress[l] = legAll[l]
        diiAllSum = 0
        totalAllVotes = 0
        votesAllAgainst = 0
        diiBillSum = 0
        totalBillVotes = 0
        votesBillAgainst = 0
        for b in votesAll[l]:
            if votesAll[l][b] == 0:
                pass
            elif votesAll[l][b] != mccarthyVotes[b]:
                diiAllSum += findDII(marginsAll[b])
                votesAllAgainst += 1
                totalAllVotes += 1
            else:
                totalAllVotes += 1
        for b in votesBill[l]:
            if votesBill[l][b] == 0:
                pass
            elif votesBill[l][b] != mccarthyVotes[b]:
                diiBillSum += findDII(marginsBill[b])
                votesBillAgainst += 1
                totalBillVotes += 1
            else:
                totalBillVotes += 1
        diiAllAvg = diiAllSum/totalAllVotes if totalAllVotes else 0
        diiBillAvg = diiBillSum/totalBillVotes if totalBillVotes else 0
    congress[l]['NumberOfAllVotes'] = totalAllVotes
    congress[l]['VotesAllAgainst'] = votesAllAgainst
    congress[l]['DIIAllSum'] = diiAllSum
    congress[l]['DIIAllAvg'] = diiAllAvg
    congress[l]['NumberOfBillVotes'] = totalBillVotes
    congress[l]['VotesBillAgainst'] = votesBillAgainst
    congress[l]['DIIBillSum'] = diiBillSum
    congress[l]['DIIBillAvg'] = diiBillAvg


del congress["B000589"]
del congress["N000186"]

dw = open("DW.DAT", "r")
bioguide_ids = json.loads(open('icpsrtobioguide.json', 'r').read())
for l in dw:
  congressN = int(l[0:4])
  district = int(l[13:16])
  if not congressN==114 or district==0:
    pass
  else:
    d1 = float(l[41:48])
    icpsr = int(l[5:11])
    bioguide = bioguide_ids[str(icpsr)]
    try:
      sunlight = urllib2.urlopen("http://congress.api.sunlightfoundation.com/legislators?bioguide_id=%(s)s&apikey=7451ff2c87114feda3967cbae344b9bb" %{"s":bioguide})
      sunlightJson = json.loads(sunlight.read())['results'][0]
      firstname = sunlightJson['first_name']
      lastname = sunlightJson['last_name']
      district = sunlightJson['state'] + "-" + str(sunlightJson['district'])
      congress[bioguide]['firstname'] = firstname
      congress[bioguide]['lastname'] = lastname
      congress[bioguide]['district'] = district
      congress[bioguide]['dw'] = d1
    except IndexError:
      try:
        del congress[bioguide]
      except KeyError:
        print "already gone"
      print "whoops!"



outFile = open("DII.json", "w")
outFile.write(json.dumps(congress))
outFile.close()



