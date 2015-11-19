#!/bin/python2
from BeautifulSoup import BeautifulSoup
import urllib2
import re

#getActions() returns a list of all actions from the 2015 session
def getActions():
    actions = []
    n = range(0,6)
    for i in n:
        num = str(i*100).zfill(3)
        page = urllib2.urlopen("http://clerk.house.gov/evs/2015/ROLL_%(n)s.asp" %{"n":num}).read()
        bs = BeautifulSoup(page)
        table = bs.find("table")
        rows = table.findAll("tr")
        rows = rows[1:]
        for r in rows:
            entries = r.findAll("td")
            voteLink = entries[0].find('a')['href']
            voteID = entries[0].text
            name = entries[2].text.replace(" ", "").lower()
            motionType = entries[3].text
            result = entries[4].text
            if int(voteID) > 2 and int(voteID) != 581:
                actions.append([voteID, voteLink, name, motionType, result])
    return actions

#filterActions() takes a list of actions from getActions() and can filter out just those votes which were on bills or just those votes that passed
def filterActions(actions, billsOnly=False, passedOnly=False):
    actionsNew = []
    for a in actions:
        nameType = " ".join(re.findall("[a-zA-Z]+", a[2]))
        passed = (a[4]=="P")
        flag = (a[3]=="On Passage" or not billsOnly) and (passed or not passedOnly)
        if flag:
            actionsNew.append(a)
    return actionsNew

#getMargins() takes a list of actions, either from getActions() or filtered through filterActions and returns the margin on each vote
def getMargins(actions):
    margins = {}
    for a in actions:
        votePage = urllib2.urlopen(a[1])
        voteBS = BeautifulSoup(votePage)
        yeas = int(voteBS.findAll('yea-total')[3].text)
        nays = int(voteBS.findAll('nay-total')[3].text)
        margin = abs(yeas-218)
        margins[a[0]] = margin
    return margins

#getVoteDict takes a list of actions and returns a dictionary where the index is the ID for a legislator. Each legislator's entry includes a 'Name' field which is their name and a 'Party' field. The rest of the fields are their vote on every action they voted on.
def getVoteDict(actions):
    votes = {}
    legislators = {}
    for a in actions:
        issue = a[0]
        votePage = urllib2.urlopen(a[1])
        voteBS = BeautifulSoup(votePage)
        voteData = voteBS.find('vote-data').findAll('recorded-vote')
        for r in voteData:
            nameID = r.find('legislator')['name-id']
            vote = r.find('vote').text
            voteNum = 1*(vote=='Aye' or vote=='Yea') + 2*(vote=='No' or vote=='Nay') + 3*(vote=="Present")
            try:
                votes[nameID][issue] = voteNum
            except KeyError:
                legislators[nameID] = {'Party':r.find('legislator')['party'], "Name":r.find('legislator').text}
                votes[nameID] = {}
                votes[nameID][issue] = voteNum
    return legislators, votes
