def bar(csv1, otptnm, cndt):

    # n = raw_input("what csv?   ")
    # d = raw_input("output name:  ")
    # e = raw_input("condition:  ")

    a = pd.read_csv(csv1)

    ax = a.plot(x="Strain", kind="bar", width=1, use_index="True")

    labels = a["Strain"]

    ax.legend(bbox_to_anchor=(1, 1.05))
    ax.set_xticks(sp.arange(len(labels)))
    ax.set_ylabel("Num of Worms")
    ax.set_xticklabels(labels, fontsize=10, rotation=45)
    titl = os.path.join("CE_GBA_07-" + cndt)
    ax.set_title(titl)

    output = os.path.join(otptnm + ".png")
    plt.savefig(output, bbox_inches="tight")
    

def sctr(csva, csvb, var1, var2):
    a = pd.read_csv(csva)
    b = pd.read_csv(csvb)

    w = a.groupby('CBE_conc').size()

    plt.scatter(x=b[var1], y=b[var2])
    plt.xticks(b[var1], w, rotation=45, fontsize=8)


    savefig('CBE_scatter-rawArea2.png', bbox_inches='tight')



### Scatter of column (wellnum) vs area
# o.plot(x='well_num', y='area', kind='scatter', title='CBE_conc_rep', legend=True, grid=True) # xlabel='well number (column)', ylabel='area'
# savefig(picoutnm, bbox_inches='tight') ## Need to repeat??
# plt.gcf().clear()

### Area vs VaroI
# picoutnm2 = os.path.join(nm + "2.png")
# dp = (o.groupby(['CBE_conc(uM)'], as_index=True).mean().groupby('CBE_conc(uM)')['area'].mean())
# pltttl = join('CBE_conc(uM)' + '_avg')
# dp.plot(title=pltttl, legend=True, grid=True)
# savefig(picoutnm2, bbox_inches='tight') 

def wskr(csv1, var1, var2):

    # nm = raw_input("Name for output:   ")
    a = pd.read_csv(csv1)
    b = csv1.split('.')

    bxplt = a.boxplot(column='area', by='BZB_conc(uM)')
    #plt.xticks(b['CBE_conc(uM)'], a['CBE_conc'])
    bxplt.set_title("Plate " + b[0] + "  " + "Strain=" + a['Strain'][1])

    outptnm = os.path.join(b[0] + ".png")

    savefig(outptnm, bbox_inches='tight')

# show()

## graphs all points in scatter using R

# def allplt(csvs):
#    for a in csvs:
#        a0 = pd.read_csv(a)
        
#        robjects.r('''                                        
#         calc.zneg <- function(x) {
#           ctrl.avgs <- x %>%
#             group_by(plt_nm) %>%
#             filter(condt == "-ctrl") %>%
#             dplyr::summarise(ctrlmean = mean(area), 
#                              ctrlstdev = sd(area)) 
#           x.zneg <- left_join(x, ctrl.avgs, by = c("plt_nm")) %>% 
#             mutate(zneg = (area - ctrlmean)/ctrlstdev) %>% 
#             select(-c(ctrlmean, ctrlstdev))
#           
#           return(x.zneg)
#         }
#         ''')
#    
#    
#        r_f = robjects.globalenv['calc.zneg'] 
#        res = r_f(a0)
#        r.data('res')
#    
#        pd_df = pandas2ri.ri2py_dataframe(res) 
#        out = a.split('.csv')
#        
#        pd_df.to_csv(a, index=False)

