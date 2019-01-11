import rpy2.robjects as robjects
from rpy2.robjects import r, pandas2ri
import pandas as pd
from rpy2.robjects.packages import importr
pandas2ri.activate()
import os

dplyr = importr('dplyr', on_conflict="warn")
utils = importr('utils')
base = importr('base')
ggplot2 = importr('ggplot2')
plotly = importr('plotly')
devtools = importr('devtools')
# forcats = importr('forcats')
dt = importr('data.table')


#calcs zneg
def zscrn(csvs):

    for a in csvs:
        a0 = pd.read_csv(a)

        robjects.r('''
         calc.zneg <- function(x) {
           ctrl.avgs <- x %>%
             group_by(rep, plt_nm) %>%
             filter(condt == "-ctrl") %>%
             dplyr::summarise(ctrlmean = mean(`O.D.`),
                              ctrlstdev = sd(`O.D.`))
           x.zneg <- left_join(x, ctrl.avgs, by = c("rep", "plt_nm")) %>%
             mutate(zneg = (`O.D.` - ctrlmean)/ctrlstdev) %>%
             select(-c(ctrlmean, ctrlstdev))

           return(x.zneg)
         }
         ''')


        r_f = robjects.globalenv['calc.zneg']
        res = r_f(a0)
        r.data('res')

        pd_df = pandas2ri.ri2py_dataframe(res)
#        out = a.split('.csv')

        pd_df.to_csv(a, index=False)

# calcs zpos
def zscrp(csvs):

    for a in csvs:
        a0 = pd.read_csv(a)

        robjects.r('''
         calc.zpos <- function(x) {
           ctrl.avgs <- x %>%
             group_by(rep, plt_nm) %>%
             filter(condt == "+ctrl") %>%
             dplyr::summarise(ctrlmean = mean(`O.D.`),
                              ctrlstdev = sd(`O.D.`))
           x.zpos <- left_join(x, ctrl.avgs, by = c("rep", "plt_nm")) %>%
             mutate(zpos = (`O.D.` - ctrlmean)/ctrlstdev) %>%
             select(-c(ctrlmean, ctrlstdev))

           return(x.zpos)
         }
         ''')


        r_f = robjects.globalenv['calc.zpos']
        res = r_f(a0)
        r.data('res')

        pd_df = pandas2ri.ri2py_dataframe(res)
#        out = a.split('.csv')

        pd_df.to_csv(a, index=False)

## summary file generator
def summr(csv):
    nm = os.path.basename(csv).split('.')
    drnm = os.path.dirname(csv)
    a = pd.read_csv(csv)
    robjects.r('''
    summr <- function(z) {
    foo <- z %>% group_by(rep, plt_nm, condt) %>%
    dplyr::summarise(mean_OD = mean(`O.D.`), median_OD = median(`O.D.`), sd_OD = sd(`O.D.`), mean_zneg = mean(zneg), sd_zneg = sd(zneg), mean_zpos = mean(zpos), sd_zpos = sd(zpos))
    }
    ''')

    r_summr = robjects.globalenv['summr']
    raz = r_summr(a)
    r.data('raz')

    pd_df = pandas2ri.ri2py_dataframe(raz)
    pd_df.to_csv((drnm + '/' + nm[0] + '_sumfile.csv'), index=False)

## summarises by plate
def summr_pl(csv):
    nm = os.path.basename(csv).split('.')
    drnm = os.path.dirname(csv)
    a = pd.read_csv(csv)
    robjects.r('''
    summr_pl <- function(z) {
    foo <- z %>% group_by(plt_nm, condt) %>%
    dplyr::summarise(mean_OD = mean(`O.D.`), median_OD = median(`O.D.`), sd_OD = sd(`O.D.`), mean_zneg = mean(zneg), sd_zneg = sd(zneg), mean_zpos = mean(zpos), sd_zpos = sd(zpos))
    }
    ''')

    r_summr_pl = robjects.globalenv['summr_pl']
    raz = r_summr_pl(a)
    r.data('raz')

    pd_df = pandas2ri.ri2py_dataframe(raz)
    pd_df.to_csv((drnm + '/' + nm[0] + '_sum_plate.csv'), index=False)

## summarises by plate
def summr_rp(csv):
    nm = os.path.basename(csv).split('.')
    drnm = os.path.dirname(csv)
    a = pd.read_csv(csv)
    robjects.r('''
    summr_rp <- function(z) {
    foo <- z %>% group_by(rep, condt) %>%
    dplyr::summarise(mean_OD = mean(`O.D.`), median_OD = median(`O.D.`), sd_OD = sd(`O.D.`), mean_zneg = mean(zneg), sd_zneg = sd(zneg), mean_zpos = mean(zpos), sd_zpos = sd(zpos))
    }
    ''')

    r_summr_rp = robjects.globalenv['summr_rp']
    raz = r_summr_rp(a)
    r.data('raz')

    pd_df = pandas2ri.ri2py_dataframe(raz)
    pd_df.to_csv((drnm + '/' + nm[0] + '_sum_condt.csv'), index=False)

## PLOTTING
#plots controls by rep by O.D.
def ctrlbx_raw(a):
    a0 = pd.read_csv(a)
    lst = []
    for i in a0['rep'][:]:
        if i not in lst:
            lst.append(i)

    robjects.r('''
        bxplta <- function(zz, aa) {
  ggplot(data = filter(zz, condt != "exp", rep==aa), aes(x = condt, y = `O.D.`)) +
    facet_grid(~plt_nm) +
    labs(title = aa,
         y = "O.D.",
         x = "Control",
         color = "condt",
         shape = "rep") +
    theme(plot.title = element_text(hjust = 0.5)) +
  geom_boxplot()
}
''')

    r_bxa = robjects.globalenv['bxplta']

    for i in range(len(lst)):
        rea = r_bxa(a0, lst[i])
        robjects.r.ggsave(filename=('../final/' + lst[i] + '_raw.png'), plot=rea, width=40, height=24, unit='cm')

## plots all

def pltall_raw(a):
    a0 = pd.read_csv(a)

    robjects.r('''
        pltala <- function(z) {
  p <- ggplot(z, aes(x = well, y = `O.D.`)) +
  geom_point(aes(color = condt, shape = rep),
             alpha = 0.6,
             size = 3) +
  facet_grid(~plt_nm) +
  scale_y_continuous(labels = scales::comma) +
  labs(title = 'All Raw O.D.',
       y = "O.D. (AU)",
       x = "well",
       color = "Condition",
       shape = "Condition") +
  theme(axis.title.x = element_blank(),
        axis.ticks.x = element_blank(),
        axis.text.x = element_blank(),
        panel.grid.major.x = element_blank())
    a = ggplotly(p)
    htmlwidgets::saveWidget(a, '../final/all_raw.html')
        }
            ''')

    r_pltala = robjects.globalenv['pltala']
    rez = r_pltala(a0)
