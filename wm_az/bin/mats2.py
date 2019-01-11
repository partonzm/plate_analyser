import os
import pandas as pd
import glob

#Auto-Excluder
def excl2(vsc, std):

    nm2 = vsc.split('.')

    stds = float(std)

    a = pd.read_csv(vsc)

    outliers = a.groupby('plt_nm').transform(lambda group: (group - group.mean()).abs().div(group.std())) > stds

    dfv = a[outliers.area == False]
    dfo = a[outliers.area == True]

    excl = os.path.join(nm2[0] + "_excl" + ".csv")
    otly = os.path.join(nm2[0] + "_Outliers" + ".csv")

    dfv.to_csv(excl)
    dfo.to_csv(otly)

## Defines calculate z-score from controls (true python)
#def ops(csvs,  ops): ## Add | appx='_operated' | for appendix

#    for a in csvs:
#        a0 = pd.read_csv(a)
#        a0[zscore] = a0.index
#        for i in range(len(a0['cond'])):
#            if a0['cond'][i] == 'exp':
#                a0[zscore][i] = # calc zscore
#            else:
#                a0[zscore][i] = 'N/A'

    ## Needs some output


## controls Exclusion (multiple files)

def exs(csvs, zexcl=2):
    for a in csvs:
        nm = a.split('.')
        a0 = pd.read_csv(a)
        g = a0.loc[(a0['condt'] == '+ctrl') & (abs(a0['zpos']) <= zecl)]
        h = a0.loc[(a0['condt'] == '-ctrl') & (abs(a0['zneg']) <= zecl)]
        i = a0.loc[(a0['condt'] == 'exp')]
        incl = pd.concat([g, h, i])

        gg = a0.loc[(a0['condt'] == '+ctrl') & (abs(a0['zpos']) > zecl)]
        hh = a0.loc[(a0['condt'] == '-ctrl') & (abs(a0['zneg']) > zecl)]
        excl = pd.concat([gg, hh])

        ex = os.path.join(nm[0] + "_excl" + ".csv")
        ot = os.path.join(nm[0] + "_Outliers" + ".csv")

        incl.to_csv(ex, index=False)
        excl.to_csv(ot, index=False)

## controls Exclusion (single file)

def ex(csv, zexcl):
    nm = os.path.basename(csv).split('.')
    a0 = pd.read_csv(csv)
    g = a0.loc[(a0['condt'] == '+ctrl') & (abs(a0['zpos']) < zexcl)]
    h = a0.loc[(a0['condt'] == '-ctrl') & (abs(a0['zneg']) < zexcl)]
    i = a0.loc[(a0['condt'] == 'exp')]
    incl = pd.concat([g, h, i])

    gg = a0.loc[(a0['condt'] == '+ctrl') & (abs(a0['zpos']) > zexcl)]
    hh = a0.loc[(a0['condt'] == '-ctrl') & (abs(a0['zneg']) > zexcl)]
    excl = pd.concat([gg, hh])

    ex = os.path.join(nm[0] + "_excl.csv")
    ot = os.path.join(nm[0] + "_Outliers.csv")

    incl.to_csv((os.path.dirname(csv) + "/" + ex), index=False)
    excl.to_csv((os.path.dirname(csv) + "/" + ot), index=False)

## defines hits

def hits(csv, a):
    nm = os.path.basename(csv).split('.')
    drnm = os.path.dirname(csv)
    a0 = pd.read_csv(csv)
    lst = []
    for i in a0['rep'][:]:
        if i not in lst:
            lst.append(i)
    for m in lst:
        gg = (a0.loc[(a0['rep'] == m) & (a0['condt'] == 'exp') & (a0['zneg'] > a)])
        gg.to_csv((drnm + '/' + nm[0] + '_' + m + '_hits.csv'), index=False)

    a = glob.glob(drnm + '/*_hits.csv')
    chunks = []
    for csv in a:
        an = pd.read_csv(csv)
        chunks.append(an)
    df = pd.concat(chunks)
    df.to_csv((drnm + '/' + nm[0] + '_all_hits.csv'), index=False)

## inbetween hits

def inb_hts(csv, mn, mx):
    nm = os.path.basename(csv).split('.')
    drnm = os.path.dirname(csv)
    a0 = pd.read_csv(csv)
    lst = []
    for i in a0['rep'][:]:
        if i not in lst:
            lst.append(i)
    for m in lst:
        gg = (a0.loc[(a0['rep'] == m) & (a0['condt'] == 'exp') & (a0['zneg'] > a) & (a0['zneg'] > a)])
        gg.to_csv((drnm + '/' + nm[0] + '_' + m + '_hits.csv'), index=False)

    a = glob.glob(drnm + '/*_hits.csv')
    chunks = []
    for csv in a:
        an = pd.read_csv(csv)
        chunks.append(an)
    df = pd.concat(chunks)
    df.to_csv((drnm + '/' + nm[0] + '_all_hits.csv'), index=False)

## defines tox

def tox(csv, b):
    nm = os.path.basename(csv).split('.')
    drnm = os.path.dirname(csv)
    a0 = pd.read_csv(csv)
    lst = []

    for i in a0['rep'][:]:
        if i not in lst:
            lst.append(i)

    for m in lst:
        #for x in range(len(a0['well'])):
        gg = (a0.loc[(a0['rep'] == m) & (a0['condt'] == 'exp') & (a0['zneg'] < b)])
        gg.to_csv((drnm + '/' + nm[0] + '_' + m + '_tox.csv'), index=False)

    a = glob.glob(drnm + '/*_tox.csv')
    chunks = []
    for csv in a:
        an = pd.read_csv(csv)
        chunks.append(an)

    df = pd.concat(chunks)
    df.to_csv((drnm + '/' + nm[0] + '_all_tox.csv'), index=False)

## autopulls

def autopl(a):
    nm = os.path.basename(a).split('.')
    drnm = os.path.dirname(a)
    a0 = pd.read_csv(a)

    uniques = a0[['plt_nm', 'well']].drop_duplicates(keep=False)
    duplicates = a0[~a0.index.isin(uniques.index)]

    duplicates.to_csv((drnm + '/' + nm[0] + '_autopull.csv'), index=False)

## technically not good data practice - gets reps from inst in file, not objective
def countr(a):
    a0 = pd.read_csv(a)
    nm = os.path.basename(a).split('.')
    drnm = os.path.dirname(a)
    reps = []

    for i in a0['rep'][:]:
        if i not in reps:
            reps.append(i)

    z = len(reps)

    counts = a0.groupby('plt_nm')['well'].value_counts().reset_index(name='rep_hits')
    mask = counts['rep_hits'] >= z
    sel = counts.loc[mask, :]
    sel.to_csv((drnm + '/' + nm[0] + '_final.csv'), index=False)

def countr1(a):
    a0 = pd.read_csv(a)
    nm = os.path.basename(a).split('.')
    drnm = os.path.dirname(a)
    reps = []

    for i in a0['rep'][:]:
        if i not in reps:
            reps.append(i)

    z = len(reps) - 1

    counts = a0.groupby('plt_nm')['well'].value_counts().reset_index(name='rep_hits')
    mask = counts['rep_hits'] >= z
    sel = counts.loc[mask, :]
    sel.to_csv((drnm + '/' + nm[0] + '_final.csv'), index=False)

## well scorer
def avgr_wscore(a, zlim):
    a0 = pd.read_csv(a)
    a1 = a0[a0['condt'] == 'exp']
    z = a1.groupby(['well_num']).agg(lambda x: x.unique().mean())
    zz = z.reset_index()
    zz = zz.rename(columns={'well_num': 'Column'})

#    fin = z.merge(i, on='well_num')

    wlsc = a1.drop(a1[a1.zneg < zlim].index)
    w = wlsc.groupby(['well_num']).well_num.agg('count')
    ww = w.to_frame(name='well_score')
    www = ww.reset_index()
    www = www.rename(columns={'well_num': 'Column'})

    final = zz.merge(www, on='Column', how='outer')
    final = final[['Column', 'well_score', 'zneg', 'zpos', 'area']]
    final.to_csv(('../final/final_Zo' + str(zlim) + '.csv'), index=False)

def well_scr_rep(a, group, zlim):
    a0 = pd.read_csv(a)
    g = group
    a1 = a0[a0['condt'] == 'exp']
    z = a1.groupby([g, 'rep']).agg(lambda x: x.unique().mean())
    #zz = z.reset_index()
    #zz = zz.rename(columns={'well_num': 'Column'})
    # fin = z.merge(i, on='well_num')

    wlsc = a1.drop(a1[a1.zneg < zlim].index)
    w = wlsc.groupby([g, 'rep'])[g].agg('count')
    ww = w.to_frame(name='well_score')
    www = ww.reset_index()
    # www = www.rename(columns={'well_num': 'Column'})

    final = z.merge(www, on=g, how='outer')
    final = final[[g, 'well_score', 'zneg', 'zpos', 'area']]
    final.to_csv(('../final/final_Zo' + str(zlim) + '.csv'), index=False)

def well_scr(a, group, zlim):
    a0 = pd.read_csv(a)
    g = group
    a1 = a0[a0['condt'] == 'exp']
    z = a1.groupby([g]).agg(lambda x: x.unique().mean())
    #zz = z.reset_index()
    #zz = zz.rename(columns={'well_num': 'Column'})
    # fin = z.merge(i, on='well_num')

    wlsc = a1.drop(a1[a1.zneg < zlim].index)
    w = wlsc.groupby([g])[g].agg('count')
    ww = w.to_frame(name='well_score')
    www = ww.reset_index()
    # www = www.rename(columns={'well_num': 'Column'})

    final = z.merge(www, on=g, how='outer')
    final = final[[g, 'well_score', 'zneg', 'zpos', 'area']]
    final.to_csv(('../final/final_Zo' + str(zlim) + '.csv'), index=False)
