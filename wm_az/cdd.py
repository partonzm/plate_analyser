import pandas as pd
import os
from bin import si_req

def cdd(fin, ht, tx):
     a0 = pd.read_csv(fin)
     b0 = pd.read_csv(ht)
     c0 = pd.read_csv(tx)

     hts = b0.drop(columns='rep_hits')
     tox = c0.drop(columns='rep_hits')
     pull = [hts, tox]
     z1 = pd.concat(pull)

     z3 = a0.merge(z1, on=('plt_nm','well'), how='left')

     z4 = z3.fillna('N/A')

## need to get a naming function in here, as well as clean up the
## column names for prettiness in CDD

     z3.to_csv(fin, index=False)

cdd('../final/all_excl.csv', '../final/all_excl_all_hits_final.csv', '../final/all_excl_all_tox_final.csv')
