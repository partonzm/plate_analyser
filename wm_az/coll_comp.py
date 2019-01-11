import os
import pandas as pd
import glob

cs = glob.glob('... *.txt')
ref = ''

def compr(csvs, ref, jcol):
    rf = pd.read_csv(ref, sep='\t')
    b = []
    for a in csvs:
         nm = a.split('.')
         a0 = pd.read_csv(a, sep='\t')

         ## c0de g0es h3re
         join_ = a0.merge(rf, on=str(jcol), how='inner')
         union_ = a0.merge(rf, on=str(jcol), how='outer')

         jn = os.path.join('./' + nm[0] + "_included" + ".txt")
         un = os.path.join('./' + nm[0] + "_excluded" + ".txt")

         join_.to_csv(jn, index=False, sep='\t')
         union_.to_csv(un, index=False, sep='\t')

compr(cs, ref, "Formula")


def compr2(csvs, ref, jcoll, jcolr):
    rf = pd.read_csv(ref, sep='\t')
    b = []
    for a in csvs:
         nm = a.split('.')
         a0 = pd.read_csv(a, sep='\t')

         ## c0de g0es h3re
         join_ = a0.merge(rf, right_on=str(jcolr), left_on=str(jcoll), how='inner')
         union_ = a0.merge(rf, right_on=str(jcolr), left_on=str(jcoll), how='outer')

         jn = os.path.join('./' + nm[0] + "_included" + ".txt")
         un = os.path.join('./' + nm[0] + "_excluded" + ".txt")

         join_.to_csv(jn, index=False, sep='\t')
         union_.to_csv(un, index=False, sep='\t')

compr2(cs, ref, "MOLENAME", "chemical_name")
