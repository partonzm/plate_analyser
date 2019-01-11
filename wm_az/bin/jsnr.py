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


def echr(a):
    nm = a.split('.')
    a0 = pd.read_csv(a)
    tail = len(a0.index) - 4 # maybe minus 3
    meat = a0.iloc[6:tail]
    meta1 = a0[:5]
    meta2 = a0[tail:]

    meta3 = meta1.append(meta2)
    meta = meta3.loc[:, ~meta3.columns.str.contains('^Unnamed')].reset_index(drop=True)

    metaT = meta.T
    metaT.columns = metaT.iloc[0]
    meta_f = metaT[1:]
    meta_fin = meta_f.loc[:, ~meta_f.columns.str.contains('^Unnamed')]
    meta_fin.to_json((nm[0] + '_meta.json'), orient='records')

#validated to here (27sept)
    meat1 = meat[1:].reset_index(drop=True)
    meat_hdr = meat.iloc[1].reset_index(drop=True)
    meat2 = meat1[2:]
    meat2.columns = meat1.iloc[0]
    meat3 = meat2.dropna(subset=['Source Plate Type'])

    ## NEED TO DROP DUPLICATE index if it exists - not tested yet (1oct18)
    meat4 = meat3[~meat3.select_dtypes(['object']).eq('Source Plate Name').any(1)]

    meat4.to_json((nm[0] + '_meat.json'), orient='records')


# .reset_index(drop=True)
#    metaT = meta.T #.reset_index()[:2]
#    metaT.columns = metaT.iloc[0]
