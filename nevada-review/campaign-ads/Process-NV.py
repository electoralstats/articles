import csv
from datetime import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import sys

mpl.rcParams['font.stretch'] = 'condensed'
mpl.rcParams['font.serif'] = ['Gentium Basic']
mpl.rcParams['font.family'] = 'serif'

def getRows():
  csvfile = open("campaign_ads.csv", "r")
  csvreader = csv.reader(csvfile,delimiter=",")
  rows = []
  for r in csvreader:
    if r[3].find("MA, USA") >= 0 or r[3].find("IA, USA") >= 0 or r[3].find("SC, USA") >= 0:
      rows.append(r)
  return rows

def processRows(rows):
  bushMonths = {}
  for r in rows:
    if r[8].find("Right To Rise USA") >= 0 or r[3].find("Jeb 2016"):
      start_time = dt.strptime(r[4], "%Y-%m-%d %H:%M:%S %Z")
      end_time = dt.strptime(r[5],  "%Y-%m-%d %H:%M:%S %Z")
      run_time = end_time - start_time
      run_days =  run_time.days
      run_seconds = run_time.seconds
      run_mins = (run_days * 24 * 60) + (run_seconds / 60.0)
      month_year = start_time.strftime("%Y-%m-%d")
      try:
        bushMonths[month_year] += run_mins
      except KeyError:
        bushMonths[month_year] = run_mins

  return bushMonths

def writeBush(bushMonths):
  bushMos = []
  bushMins = []
  for key in bushMonths:
    bushMos.append(key)
    bushMins.append(bushMonths[key])
  bushList = [[dt.strptime(y, "%Y-%m-%d"),x] for (y,x) in sorted(zip(bushMos, bushMins))]
  return bushList

def plotBush(bushList):
  x = [x[0] for x in bushList]
  y = [x[1] for x in bushList]
  fig = plt.figure(figsize=(8,4))
  ax = fig.add_axes((.1, .8, .8, .9))
  plt.scatter(x,y, c="#1185D7", marker='.', lw=0, s=130)
  plt.ylim([0, 2000])
  plt.xlabel("Date")
  plt.ylabel("Minutes of Advertising")
  plt.xticks(rotation="vertical")
  plt.title("Bush Advertising in IA, NH and SC")
  plt.figtext(.1, .43, 'ElectoralStatistics.com', color='#283D4B', ha='left')
  plt.figtext(.9, .43, 'Source: Political TV Ad Archive', color='#283D4B', ha='right')
  plt.savefig("bush_ads.png", bbox_inches="tight")
  
rows = getRows()
bushMonths = processRows(rows)
bushList = writeBush(bushMonths)
plotBush(bushList)
