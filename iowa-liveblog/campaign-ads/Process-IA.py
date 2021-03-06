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
    if not r[3].find("IA, USA") < 0:
      rows.append(r)
  return rows

def processRows(rows):
  candidates = {}
  for row in rows:
    name = row[8].replace(" (candcmte)", "")
    start_time = dt.strptime(row[4], "%Y-%m-%d %H:%M:%S")
    end_time = dt.strptime(row[5], "%Y-%m-%d %H:%M:%S")
    run_time = end_time - start_time
    run_days = run_time.days
    run_seconds = run_time.seconds
    run_mins = (run_days * 24 * 60) + (run_seconds / 60.0)
    try:
      current = candidates[name]
      candidates[name] = current + run_mins
    except KeyError:
      candidates[name] = run_mins
  return candidates

def sortCandidates(candidates):
  cancom = {}
  pacs = {}
  for key in candidates:
    if not key.find("SuperPAC") < 0:
      newKey = key.replace(" (SuperPAC)", "")
      pacs[newKey] = candidates[key]
    else:
      newKey = candidateGroups[key]
      cancom[newKey] = candidates[key]
  return cancom, pacs

def plot(candidates, spec):
  data = candidates
  categories = [key for key in data]
  values = [data[key] for key in data]
  categories = [x for (y,x) in sorted(zip(values, categories), key=lambda pair: pair[0])]
  values = sorted(values)
  fig = plt.figure(figsize=(8,4))
  ax = fig.add_axes((.1, .8, .8, .9))
  pos = np.arange(len(categories)) + .5
  rects = ax.barh(pos, values, align='center', color=spec['color'], edgecolor=spec['color'])
  for i in range(0,len(rects)):
    r = rects[i]
    length = r.get_width()
    alignment = 'right' if values[i]<0 else 'left'
    if spec['decimals']:
      valString = '{0:.1f}'.format(values[i])
    else:
      valString = int(values[i])
    ax.text(values[i] + (1*r.get_height())*((values[i]+0.0001)/abs(values[i]+0.0001)), r.get_y()+r.get_height()/2, valString, ha=alignment, va='center')
  plt.yticks(pos, categories)
  plt.ylabel(spec['ylabel'])
  plt.xlabel(spec['xlabel'])
  if spec['lims']:
      plt.xlim(spec['lims'])
  plt.title(spec['title'])
  plt.figtext(.1, .63, 'ElectoralStatistics.com', color='#283D4B', ha='left')
  if spec['source']:
    plt.figtext(.9, .63, 'Source: ' + spec['source'], color='#283D4B', ha='right')
  plt.savefig(spec['outfile'], bbox_inches='tight')



spec = {"title":"Who is Advertising in Iowa",
        "xlabel":"Minutes of TV Ads",
        "ylabel":"",
        "type":"barplot",
        "color":"#1185D7",
        "regresscolor":"#1185D7",
        "linecolor":"#1185D7",
        "colors":["#1185D7", "#54A7E2", "#22435A"],
        "regress":False,
        "connect":False,
        "delimiter":" ",
        "source":"Political TV Ad Archive",
        "lims":[0,6200],
        "plots":1,
        "ylabels":["","","","","","","",""],
        "xlabels":["","","","","","","",""],
        "decimals":True,
        "line":False,
        "outfile":"ads-ia.png",
        "add_axes":False,
}

candidateGroups = {
  "Hillary for America": "Hillary Clinton",
  "Bernie 2016": "Bernie Sanders",
  "Marco Rubio for President": "Marco Rubio",
  "Donald J. Trump For President": "Donald Trump",
  "Cruz For President": "Ted Cruz",
  "Carson America": "Ben Carson",
  "Kasich For America": "John Kasich",
  "Carly for President": "Carly Fiorina",
  "Rand Paul for President": "Rand Paul",
  "Chris Christie For President Inc": "Chris Christie",
  "Huckabee For President": "Mike Huckabee",
  "Lindsey Graham 2016": "Lindsey Graham",
  "O'Malley For President": "Martin O'Malley",
  "Jeb 2016": "Jeb Bush"
}
rows = getRows()
allCands = processRows(rows)
cands, pacs = sortCandidates(allCands)
spec['title'] = "Who is Advertising in Iowa: Candidates"
spec['outfile'] = "ads-ia-candidates.png"
plot(cands, spec)
spec['title'] = "Who is Advertising in Iowa: SuperPACs"
spec['outfile'] = "ads-ia-pacs.png"
spec['lims'] = [0,2000]
plot(pacs, spec)
