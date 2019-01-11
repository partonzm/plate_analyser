## cleans up csv's names
import os
import pandas as pd

## This is the place for methods dealing with the shuttling of data inside csvs with pandas
## things should be written to accept glob inputs


## Merges CSVs blind
def mrgr(a):
    chunks = []
    for csv in a:
        an = pd.read_csv(csv)
        chunks.append(an)
    df = pd.concat(chunks)
    df.to_csv('../final/all.csv', index=False)


## naming stuffs. pretty sure all three fun below (maybe more) can be combined to one
def repsplit(a):
    for f in a:
        yy = os.path.basename(f).split('_')
        os.rename(f, os.path.join(os.path.dirname(f), (yy[3] + '.csv')))

## injects src file name
def pltnmij(a):
    for csv in a:
        frame = pd.read_csv(csv)
        frame['src_file'] = os.path.basename(csv)
        frame.to_csv(csv, index=False)

##needs to be optimized
def pltnmr(a):
    for csv in a:
        a0 = pd.read_csv(csv)
        a0['plt_nm'] = a0.index
        for i in range(len(a0['src_file'])):
            intr = a0['src_file'][i].split('.')
            a0['plt_nm'][i] = intr[0]
        a0.to_csv(csv, index=False)

## injects rep#

def repij(a):
    for csv in a:
        a0 = pd.read_csv(csv)
        a0['rep'] = a0.index
        path=os.path.dirname(csv)
        for i in range(len(a0['well'])):
            a0['rep'][i] = os.path.basename(path)
        a0.to_csv(csv, index=False)

def rep_insert(a):
    for csv in a:
        a0 = pd.read_csv(csv)
        a0['rep'] = a0.index
        path=os.path.dirname(csv)
        a0['rep'] = os.path.basename(path)
        a0.to_csv(csv, index=False)

class nmr:
    def rep(a):
        for csv in a:
            a0 = pd.read_csv(csv)
            path=os.path.dirname(csv)
            a0['rep'] = a0.apply(lambda row: os.path.basename(path))
            a0.to_csv(csv, index=False)

    def pltnmr(a):
        for csv in a:
            a0 = pd.read_csv(csv)
            a0['plt_nm'] = a0.index
            for i in range(len(a0['src_file'])):
                intr = a0['src_file'][i].split('.')
                a0['plt_nm'][i] = intr[0]
            a0.to_csv(csv, index=False)

## Creates well_letter and well_number variables
## slow code
def idxr(a):
    for csv in a:
        a1 = pd.read_csv(csv)
        a1['well_let'] = a1.index
        a1['well_num'] = a1.index

        for i in range(len(a1['well'])):
            a1['well_let'][i] = a1['well'][i][0]
            a1['well_num'][i] = a1['well'][i][1:]
        a1.to_csv(csv, index=False)

## fast code
def well_idxr(files):
    for csv in files:
        a0 = pd.read_csv(csv)
        a0['well_letter'] = a0.apply(lambda row: row.well[0], axis=1)
        a0['well_number'] = a0.apply(lambda row: row.well[1:], axis=1)
        a0.to_csv(csv, index=False)

## needs to be optimized
## annotates ctrls
def annt(a):
    for csv in a:
        a1 = pd.read_csv(csv)
        a1['condt'] = a1.index
        for i in range(len(a1['well_number'])):
            if a1['well_number'][i] == 1:
                a1['condt'][i] = "+ctrl"
            elif a1['well_number'][i] == 2:
                 a1['condt'][i] = "+ctrl"
            elif a1['well_number'][i] == 23:
                 a1['condt'][i] = "-ctrl"
            elif a1['well_number'][i] == 24:
                 a1['condt'][i] = "-ctrl"
            else:
                 a1['condt'][i] = "exp"
            a1.to_csv(csv, index=False)

def yt_annt(a):
    for csv in a:
        a1 = pd.read_csv(csv)
        a1['condt'] = a1.index
        for i in range(len(a1['well_number'])):
            if a1['well_number'][i] == 1:
                a1['condt'][i] = "+ctrl"
            elif a1['well_number'][i] == 2:
                 a1['condt'][i] = "-ctrl"
            elif a1['well_number'][i] == 23:
                 a1['condt'][i] = "-ctrl"
            elif a1['well_number'][i] == 24:
                 a1['condt'][i] = "+ctrl"
            else:
                 a1['condt'][i] = "exp"
            a1.to_csv(csv, index=False)

## NEEDS TO BE OPTIMIZED
def better_annt(a):
    for csv in a:
        a1 = pd.read_csv(csv)
        a1['condt'] = a1.index
        for i in range(len(a1['well_number'])):
            if a1['well_number'][i] in range(1, 2):
                a1['condt'][i] = "+ctrl"
            elif a1['well_number'][i] in range (23, 24):
                 a1['condt'][i] = "-ctrl"
            else:
                 a1['condt'][i] = "exp"
            a1.to_csv(csv, index=False)

## annotates ctrls and columns

# def annt2(a):
#    for csv in a:
#        a1 = pd.read_csv(csv)
#        a1['condt'] = a1.index
#        for i in range(len(a1['well_num'])):
#            if a1['well_num'][i] <= 2:
#                 a1['condt'][i] = "+ctrl"
#            elif a1['well_num'][i] >= 23:
#                 a1['condt'][i] = "-ctrl"
#            elif a1['well_num'][i] == 24:
#            else:
#                 a1['condt'][i] = "exp"
#            a1.to_csv(csv, index=False)

## changes column names and does drops
def clnrr(a):
    for csv in a:
        a1 = pd.read_csv(csv)
        a1 = a1.rename(columns={'plate_id': 'date'})
        a1 = a1.drop(columns={'z_score', 'src_file'})
        a1.to_csv(csv, index=False)


def clnr2(a):
    for csv in a:
        a1 = pd.read_csv(csv)
        cols = ['rep', 'plt_nm', 'well', 'condt', 'area', 'zneg', 'zpos', 'date', 'well_letter', 'well_number']
        a2 = a1[cols]
        a2.to_csv(csv, index=False)


#def clncdd(a):
#    a1 = pd.read_csv(csv)
#    a1 = a1.drop(columns={'src_file', 'z_score', 'well_let', 'well_num'})
#    cols = ['rep', 'plt_nm', 'well', 'condt', 'area', 'zneg', 'zpos']
#    a2 = a1[cols]
#    a2.to_csv(csv, index=False)
