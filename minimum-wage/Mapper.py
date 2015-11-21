import csv
from bs4 import BeautifulSoup
from colour import Color
import numpy as np

wageColumn = 2

def getWages():
  csvFile = open("wages.csv", "r")
  csvcontents = csv.reader(csvFile, delimiter=",")
  wages = [x for x in csvcontents]
  return wages


def getColor(wage):
  if float(wage) < colorRanges[0]:
    return colors[0]
  for r in range(0,len(colorRanges)-1):
    if colorRanges[r-1] <= float(wage) <= colorRanges[r]:
      return colors[r]
  return colors[len(colors)-1]

def produceMap(wages, column, fileName, colors):
  relevantWage = [float(w[column]) for w in wages]
  wageMap = open("counties2.svg")
  mapSoup = BeautifulSoup(wageMap, "xml")
  for w in wages:
    county = mapSoup.find(attrs={"class":"c%(county)s" %{"county":w[0]}})
    try:
      county['style'] = "fill:" + str(getColor(w[column]).hex)
    except TypeError:
      print("whoops! ", w)

  gradient = mapSoup.defs.linearGradient
  ranges = np.linspace(0,1,len(colors))
  colors.reverse()
  for c in range(0,len(colors)):
    style = "stop-color:%(color)s;stop-opacity:1" %{"color":colors[c]}
    offset = str(ranges[c])
    stop = mapSoup.new_tag("stop", style=style, offset=offset)
    gradient.append(stop)
  rect = mapSoup.find(id="gradrect")
  rectX = float(rect['x'])
  rectW = float(rect['width'])
  rectY = float(rect['y'])
  rectH = float(rect['height'])
  disp = 5
  labelPos = np.linspace(0.0, rectH, 5)
  labels = np.linspace(7.25, 15.00, 5)[::-1]
  for i in range(0,len(labelPos)):
    label = mapSoup.new_tag("text", x=rectX + rectW + disp, y=rectY + labelPos[i])
    label['font-family'] = "sans"
    label['font-size'] = 12
    label.string = "${0:.2f}".format(labels[i])
    mapSoup.svg.append(label)
  outputFile = open(fileName, "w")
  outputFile.write(mapSoup.prettify())
  outputFile.close()

wages = getWages()
wageOfConcern = [float(w[wageColumn]) for w in wages]
colorRanges = np.linspace(7.25, 15.00, 30)
green = Color("blue")
red = Color("#FF0000")
colors = list(green.range_to(red, len(colorRanges)+1))
map2 = produceMap(wages, wageColumn, "countiesWage_living.svg", colors)
