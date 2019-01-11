import os
import pandas as pd
import numpy as np


def autopl2(a):
    nm = os.path.basename(a).split('.')
    drnm = os.path.dirname(a)
    a0 = pd.read_csv(a)

    unq = a0[['plt_nm', 'well']].drop_duplicates(keep=False)
    df3 = a0[~a0.index.isin(unq.index)]
    df4 = df3.drop_duplicates(subset='well', keep='last')
    df5 = df3[~df3.isin(df4)].dropna()
    unq2 = df5[['plt_nm', 'well']].drop_duplicates(keep=False)
    df6 = df3[~df3.index.isin(unq2.index)]

    df6.to_csv((drnm + '/' + nm[0] + '_autopull_hits2.csv'), index=False)

    # df3 = df3[~df3.index.duplicated(keep='first')]

        reps = []

        for i in a0['rep'][:]:
            if i not in reps:
                reps.append(i)


                def autopl2(a):
                    nm = os.path.basename(a).split('.')
                    drnm = os.path.dirname(a)
                    a0 = pd.read_csv(a)
                    reps = []

                    for i in a0['rep'][:]:
                        if i not in reps:
                            reps.append(i)

                    for i in reps[:]:
                        uniques = a0[['plt_nm', 'well']].drop_duplicates(keep=False)

                        duplicates = a0[~a0.index.isin(uniques.index)]


                    duplicates.to_csv((drnm + '/' + nm[0] + '_autopull2.csv'), index=False)
