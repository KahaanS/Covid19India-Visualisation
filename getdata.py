from urllib.request import urlopen
import ssl
import json
import os

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

fhand = open('spider.js','w')

url = 'https://api.covid19india.org/raw_data.json'
patients = json.loads(urlopen(url, context=ctx).read())['raw_data']
patdict = dict()
patnotes = dict()
finpat = list()
stats = dict()

ctr = 1

for idx, patient in enumerate(patients):
    if patient['currentstatus'] == '':
        continue
    patdict['P'+str(idx+1)] = patient['contractedfromwhichpatientsuspected']
    try:
        patnotes['P'+str(idx+1)] = patient['_d180g'] +'. '+ patient['backupnotes']+'. Status: '+patient['currentstatus']
    except:
        patnotes['P'+str(idx+1)] = patient['backupnotes']+'. Status: '+patient['currentstatus']
    finpat.append(patient)
    try:
        stats[patient['currentstatus']] = stats[patient['currentstatus']]+1
    except:
        stats[patient['currentstatus']] = 1


fhand.write('spiderJson = {"nodes":[\n')
for pid, pinfect in patdict.items():

    if pid != 'P1':
        fhand.write(',\n')

    fhand.write('{'+'"weight":'+'3000'+',')
    fhand.write(' "id":'+str(abs(int(pid[1:])))+', "url":"'+patnotes[pid]+'"}')
    ctr = ctr+1

fhand.write('],\n')

comstop = 1
fhand.write('"links":[\n')
pats = list()
for pid, pinfect in patdict.items():
    if ',' in pinfect:
        pats.append(pinfect.split(', ')[0])
    else:
        pats.append(pinfect)

    for pat in pats:

        pat1_id = pid
        pat2_id = pat

        if pat == '':
            continue

        if comstop != 1:
            fhand.write(',\n')

        comstop = comstop+1
        #fhand.write('{"source":'+pat[1:]+',"target":'+pid[1:]+',"value":3}')
        fhand.write('{"source":'+str(abs(int(pat[1:])-1))+',"target":'+str(abs(int(pid[1:])-1))+',"value":3}')

    pats.clear()

fhand.write(']};')
fhand.write('updated')
fhand.close()

statstr = ''
for tag, stat in stats.items():
    statstr = statstr + ' | ' + tag + ': ' + str(stat)

fhand = open('force.html','w')
fhand.write('<!DOCTYPE html>\n')
fhand.write('<html>\n')
fhand.write('   <head>\n')
fhand.write('       <title>COVID19 Cases - India</title>\n')
fhand.write('       <script type="text/javascript" src="d3.v2.js"></script>\n')
fhand.write('       <script type="text/javascript" src="spider.js"></script>\n')
fhand.write('       <link type="text/css" rel="stylesheet" href="force.css"/>\n')
fhand.write('   </head>\n')
fhand.write('   <body style="font-family: sans-serif;" bgcolor = "black">\n')
fhand.write('       <h1>COVID19 Cases In India - Cluster </h1>\n')
fhand.write('       <h2>Hover over a patient or link to read details.</h2>\n')
#fhand.write('       <h2>Total cases: ' + str(len(finpat))+ ' ' + statstr + '</h2>\n')
fhand.write('       <h2>Total cases: ' + str(len(finpat))+'</h2>\n')
fhand.write('       <div id="chart" style="border:1px" align="center">\n')
fhand.write('           <script type="text/javascript" src="force.js"></script>\n')
fhand.write('       </div>\n')
fhand.write('   </body>\n')
fhand.write('</html>\n')

fhand.close()

os.system('open force.html')
