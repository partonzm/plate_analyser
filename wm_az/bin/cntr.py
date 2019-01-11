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
    sel.to_csv((drnm + '/' + nm[0] + '_final_hits.csv'), index=False)
