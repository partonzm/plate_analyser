import csv
import json
import os
import pandas as pd

#def jsnr(a):
#    nm = a.split('.')
#    a0 = pd.read_csv(a)
#    b = a0.
#    a1 = open(a, 'r')
#    jsn = open((nm[0] + '.json'), 'w')
#    col = list(a0.columns)
#    reader = csv.DictReader(a1, col)
#
#    for row in reader:
#        json.dump(row, jsn)
#        jsn.write('\n')

def jsnr2(a):
    nm = a.split('.')
    a0 = pd.read_csv(a)
    a0.to_json((nm[0] + '.json'), orient='records')
