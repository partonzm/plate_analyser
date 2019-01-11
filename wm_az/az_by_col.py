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

##########
## INIT ##
##########

# variables
zhlim = 0 ## hit limit
ztlim = 0 ## tox limit
zxlim = 1.25 ## ctrl exclusion

## initial data shuttling
os.mkdir('../final')
# os.mkdir('../final/plots')
shutil.move('../data', '../final/')
os.mkdir('../data')

## __Import data Recursively through folders__
# repX = raw("which replicate?")
aa = glob.glob('../final/data/*.csv')


#clnr.pltnmij(aa)
#clnr.pltnmr(aa)
#clnr.clnrr(aa)
#clnr.idxr(aa)
#clnr.annt(aa)
by_col.zscrn(aa)
by_col.zscrp(aa)
by_col.clnr2(aa)
clnr.mrgr(aa)

## DO NOT USE IF EXCLUSION DROPS YOU BELOW 20 SAMPLES TOTOAL
mats2.ex('../final/all.csv', zxlim)

dd = glob.glob('../final/*_excl.csv')
by_col.zscrn(dd)
by_col.zscrp(dd)

# by_col.hits('../final/all_excl.csv', zplim)

a = '../final/all.csv'


# SUMS
by_col.summr(a)
# by_col.summr(b)
by_col.summr_ov_cd(a)
# by_col.summr_ov_cd(b)

# by_col.ctrlbxa(b)
by_col.ctrlbxz(a)
by_col.ctrlbxa(a)

by_col.pltala(a)
by_col.pltalz(a)

by_col.pltalmpl(a, zhlim)

mats2.avgr_wscore(a, zhlim)

## __Finishing__
# a = 'hit limit = ' + str(zplim)
# b = 'tox limit = ' + str(znlim)
# c = 'excl limit = ' + str(zxlim)
d = 'Analysis done at: ' + str(datetime.datetime.now())
f = open('../final/meta.txt', 'w')
f.write(d) # a + '\n' + b + '\n' + c + '\n' +
f.close()
