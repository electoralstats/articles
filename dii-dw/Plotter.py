import json
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams['font.stretch'] = 'condensed'
mpl.rcParams['font.serif'] = ['Gentium Basic']
mpl.rcParams['font.family'] = 'serif'

def getPoints():
  jsonFile = open('DII.json', 'r')
  congress = json.loads(jsonFile.read())
  return congress

def plot(congress):
  repubsDii = []
  demsDii = []
  repubsDw = []
  demsDw = []
  for c in congress:
    if congress[c]['Party'] == 'R':
      repubsDii.append(congress[c]['DIIAllAvg'])
      repubsDw.append(congress[c]['dw'])
    else:
      demsDii.append(congress[c]['DIIAllAvg'])
      demsDw.append(congress[c]['dw'])
  fig = plt.figure(figsize=(8,4))
  ax = fig.add_axes((.1, .8, .8, .9))
  plt.scatter(demsDw, demsDii, color="#0000ff", marker='.', lw=0, s=100)
  plt.scatter(repubsDw, repubsDii, color="#ff0000", marker='.', lw=0, s=100)
  plt.xlabel('DW-Nominate')
  plt.ylabel('DII Average (All)')
  plt.xlim(-1, 1)
  ax.annotate("More Liberal", xy=(-0.55,-4), xytext=(-0.05, -4), horizontalalignment="right", verticalalignment='center', arrowprops=dict(facecolor="black", arrowstyle="->"))
  ax.annotate("More Conservative", xy=(0.55, -4), xytext=(0.05, -4), horizontalalignment="left", verticalalignment='center', arrowprops=dict(facecolor="black", arrowstyle="->"))
  ax.annotate("More Dissenting Votes", xy=(-0.95, 25), xytext=(-0.95, -4), rotation='vertical', horizontalalignment='center', verticalalignment='bottom', arrowprops=dict(facecolor="black", arrowstyle="->"))
  plt.figtext(.1, .63, 'ElectoralStatistics.com', color='#283D4B', ha='left')
  plt.savefig("charts/master.png", bbox_inches="tight")
  plt.close(fig)
  for c in congress:
    fig = plt.figure(figsize=(8,4))
    ax = fig.add_axes((.1, .8, .8, .9))
    plt.scatter(demsDw, demsDii, color="#0000ff", marker='.', lw=0, s=100)
    plt.scatter(repubsDw, repubsDii, color="#ff0000", marker='.', lw=0, s=100)
    color = "#990000" if congress[c]['Party']=='R' else '#000099'
    plt.scatter(congress[c]['dw'], congress[c]['DIIAllAvg'], color=color, lw=0, s=125)
    textCoord = (-.5, 27) if congress[c]['Party']=='D' else (.65, 27)
    ax.annotate(congress[c]['firstname'] + " " + congress[c]['lastname'] + "\nDW-Nominate: " + '{0:.3f}'.format(congress[c]['dw']) + "\nDII Average: " + '{0:.3f}'.format(congress[c]['DIIAllAvg']), xy=(congress[c]['dw'], congress[c]['DIIAllAvg']), xytext=textCoord, horizontalalignment='center')
    ax.annotate("", xy=(congress[c]['dw'], congress[c]['DIIAllAvg']), xytext=textCoord, arrowprops=dict(facecolor="black", arrowstyle="->"))
    plt.xlabel('DW-Nominate')
    plt.ylabel('DII Average (All)')
    plt.xlim(-1, 1)
    ax.annotate("More Liberal", xy=(-0.55,-4), xytext=(-0.05, -4), horizontalalignment="right", verticalalignment='center', arrowprops=dict(facecolor="black", arrowstyle="->"))
    ax.annotate("More Conservative", xy=(0.55, -4), xytext=(0.05, -4), horizontalalignment="left", verticalalignment='center', arrowprops=dict(facecolor="black", arrowstyle="->"))
    ax.annotate("More Dissenting Votes", xy=(-0.95, 25), xytext=(-0.95, -4), rotation='vertical', horizontalalignment='center', verticalalignment='bottom', arrowprops=dict(facecolor="black", arrowstyle="->"))
    plt.figtext(.1, .63, 'ElectoralStatistics.com', color='#283D4B', ha='left')
    plt.savefig("charts/" + c + ".png", bbox_inches="tight")
    plt.close(fig)

congress = getPoints()
plot(congress)

