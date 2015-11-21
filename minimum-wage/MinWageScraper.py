import csv
from BeautifulSoup import BeautifulSoup
import urllib2

def getFIPS():
  csvFile = open("counties.csv", "r")
  csvcontents = csv.reader(csvFile, delimiter=",")
  fips = [x[1]+x[2] for x in csvcontents]
  return fips

def getData(fips):
  wages = {}
  for f in fips:
    page = urllib2.urlopen("http://livingwage.mit.edu/counties/%(county)s" %{"county":f}).read()
    soup = BeautifulSoup(page)
    table = soup.find("table")
    tableRows = table.tbody.findAll("tr")
    lw = float(tableRows[0].findAll('td')[1].text.replace("$",""))
    mw = float(tableRows[2].findAll('td')[1].text.replace("$",""))
    diff = lw-mw
    wages[f] = [mw, lw, diff]
  return wages

def writeCSV(wages):
  csvFile = open("wages.csv", "w")
  dataWriter = csv.writer(csvFile, delimiter=",")
  for w in wages:
    values = [w, wages[w][0], wages[w][1], wages[w][2]]
    dataWriter.writerow(values)
  csvFile.close()

