#!/bin/bash/python2
import urllib2
import json
import csv

'''dw = open("DW.DAT", "r")
codes = {}
whoops = open("whoops.txt", "w")
for l in dw:
  congress = int(l[0:4])
  district = int(l[13:16])
  if not congress==114 or district==0:
    pass
  else:
    icpsr = int(l[5:11])
    d2 = float(l[48:55])
    #print l
    #print icpsr
    #urll = "http://congress.api.sunlightfoundation.com/legislators?icpsr_id=%(s)i&apikey=7451ff2c87114feda3967cbae344b9bb" %{"s":icpsr}
    #print urll
    sunlight = urllib2.urlopen("http://congress.api.sunlightfoundation.com/legislators?icpsr_id=%(s)i&apikey=7451ff2c87114feda3967cbae344b9bb" %{"s":icpsr})
    sunlightJson = json.loads(sunlight.read())['results']
    if not sunlightJson:
      print icpsr
      whoops.write(str(icpsr) + "\n")
    else:
      bioguide = sunlightJson[0]['bioguide_id']
      codes[icpsr] = bioguide

jsonfile = open("icpsrtobioguide.json", "w")
jsonfile.write(json.dumps(codes))
jsonfile.close()
whoops.close()'''

jsonfile = open('icpsrtobioguide.json', 'r')
legdict = json.loads(jsonfile.read())
jsonfile.close()
whoopsfile = open("whoops2.txt", "r")
whoops = csv.reader(whoopsfile, delimiter=' ')
for l in whoops:
  try:
    bio = l[1]
    legdict[l[0]] = bio
  except IndexError:
    print l
    pass
jsonfile = open('icpsrtobioguide.json', 'w')
jsonfile.write(json.dumps(legdict))
jsonfile.close()
