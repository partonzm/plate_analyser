#!/usr/bin/env python
# -*- coding: utf-8 -*-

# """WORMSSSSSS!"""

## __Import__
import pandas as pd
import matplotlib.pyplot as plt
import os
import glob
import csv
import numpy as np
import scipy as sp
import shutil
import datetime
from pylab import figure, axes, pie, title, show, savefig
# from bin import csvs
from bin import mats2
from bin import clnr
from bin import grph
from bin import rscrps
from bin import by_col

## enviromental variables
# zhlim = 2 ## hit limit
# ztlim = -2 ## tox limit
# zxlim = 2 ## ctrl exclusion

## __verify structure__

## initial data shuttling
os.mkdir('../final')
# os.mkdir('../final/plots')
shutil.move('../data', '../final/')
os.mkdir('../data')

## __Import data Recursively through folders__
# repX = raw("which replicate?")
aa = glob.glob('../final/data/*/*.csv')

## __Clean up__
##	_linearize_
## _platenames_
clnr.repsplit(aa)
bb = glob.glob('../final/data/*/*.csv')
clnr.pltnmij(bb)
clnr.pltnmr(bb)
## injects rep names
clnr.rep_insert(bb)
## _drops,changes_
clnr.clnrr(bb)
##  _well_let/num_
clnr.well_idxr(bb)
#  _annotate +/-ctrls_
# clnr.annt(bb)

## START FROM HERE WITH ANNT

## __Calculations__
# calculates z-score
rscrps.zscrn(bb)
rscrps.zscrp(bb)

## cln again
clnr.clnr2(bb)

## _Creates master csv_
clnr.mrgr(bb)

#Remove CTRL Outliers (Automatic exclusion) (need to do recursively by plate)
# mats2.ex('../final/all.csv', zxlim)

# re-calculates z-score after exclusion
# dd = glob.glob('../final/*_excl.csv')
# rscrps.zscrn(dd)
# rscrps.zscrp(dd)

## __Hit&Tox__
# mats2.hits('../final/all_excl.csv', zhlim)
# mats2.tox('../final/all_excl.csv', ztlim)
# mats2.countr('../final/all_excl_all_hits.csv')
# mats2.countr('../final/all_excl_all_tox.csv')
#mats2.autopl('../final/all_excl_all_hits.csv')
#mats2.autopl('../final/all_excl_all_tox.csv')
#mats2.autopl2('../final/all_excl_all_hits.csv')
#mats2.autopl2('../final/all_excl_all_tox.csv')

## Correlate Echo exceptions

## Plotting & Sum
a = '../final/all.csv'


### BY COL ###
## SUMS
by_col.summr(a)
by_col.summr_ov_cd(a)
##PLOTTING
by_col.ctrlbxz(a)
by_col.ctrlbxa(a)
by_col.pltala(a)
by_col.pltalz(a)


## NORMAL PLOTTING
## Generate summaries
rscrps.summr(a)
rscrps.summr_pl(a)
rscrps.summr_rp(a)
## box plots of ctrls_
rscrps.ctrlbxz(a)
rscrps.ctrlbxa(a)
## raw area plots
rscrps.pltala(a)
## all zscore plots
rscrps.pltalz(a)
## plots mean lines

# mats2.avgr_wscore(a)

## exp zscore w/perplate & rep mean o/ctrls

## __Finishing__
d = 'Analysis done at: ' + str(datetime.datetime.now())
f = open('../final/meta.txt', 'w')
f.write(d)
f.close()
