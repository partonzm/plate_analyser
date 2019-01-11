import pandas as pd
import matplotlib.pyplot as plt
import os
import glob
import csv
import numpy as np
import scipy as sp
import shutil
import datetime

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



def zscrn(csvs):

     for a in csvs:
         a0 = pd.read_csv(a)

         robjects.r('''
          calc.zneg <- function(x) {
            ctrl.avgs <- x %>%
              group_by(plt_nm) %>%
              filter(condt == "-ctrl") %>%
              dplyr::summarise(ctrlmean =  mean(area),
                               ctrlstdev = sd(area))
            x.zneg <- left_join(x, ctrl.avgs, by = c("plt_nm")) %>%
              mutate(zneg = (area - ctrlmean)/ctrlstdev) %>%
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

def clnr2(a):
     for csv in a:
         a1 = pd.read_csv(csv)
         cols = ['plt_nm', 'well', 'condt', 'area', 'zneg', 'zpos', 'date', 'well_let', 'well_num']
         a2 = a1[cols]
         a2.to_csv(csv, index=False)

def zscrp(csvs):

     for a in csvs:
         a0 = pd.read_csv(a)

         robjects.r('''
          calc.zpos <- function(x) {
            ctrl.avgs <- x %>%
              group_by(plt_nm) %>%
              filter(condt == "+ctrl") %>%
              dplyr::summarise(ctrlmean = mean(area),
                               ctrlstdev = sd(area))
            x.zpos <- left_join(x, ctrl.avgs, by = c("plt_nm")) %>%
              mutate(zpos = (area - ctrlmean)/ctrlstdev) %>%
              select(-c(ctrlmean, ctrlstdev))
            return(x.zpos)
          }
          ''')


         r_f = robjects.globalenv['calc.zpos']
         res = r_f(a0)
         r.data('res')

         pd_df = pandas2ri.ri2py_dataframe(res)

         pd_df.to_csv(a, index=False)

def hits(csv, a):
     nm = os.path.basename(csv).split('.')
     drnm = os.path.dirname(csv)
     a0 = pd.read_csv(csv)
     gg = (a0.loc[(a0['condt'] == 'exp') & (a0['zneg'] > a)])
     gg.to_csv((drnm + '/' + nm[0] + '_' + 'hits.csv'), index=False)

def ctrlbxa(a):
    a0 = pd.read_csv(a)
    lst = []
    for i in a0['plt_nm'][:]:
        if i not in lst:
            lst.append(i)

    robjects.r('''
        bxplta <- function(zz, aa) {
  ggplot(data = filter(zz, condt != "exp", plt_nm==aa), aes(x = condt, y = area)) +
    labs(title = aa,
         y = "Area",
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
        robjects.r.ggsave(filename=('../final/' + str(lst[i]) + '_BY-COL_raw.png'), plot=rea, width=40, height=24, unit='cm')

def ctrlbxz(a):
    a0 = pd.read_csv(a)
    lst = []
    for i in a0['plt_nm'][:]:
        if i not in lst:
            lst.append(i)

    robjects.r('''
        bxpltz <- function(zz, aa) {
  ggplot(data = filter(zz, condt != "exp", plt_nm==aa), aes(x = condt, y = zneg)) +
    labs(title = aa ,
         y = "Zscore w/r/t -CTRL",
         x = "Control",
         color = "condt",
         shape = "rep") +
    theme(plot.title = element_text(hjust = 0.5)) +
  geom_boxplot()
}
''')

    r_bxz = robjects.globalenv['bxpltz']

    for i in range(len(lst)):
        rez = r_bxz(a0, lst[i])
        robjects.r.ggsave(filename=('../final/' + str(lst[i]) + '_BY-COL_zscore.png'), plot=rez, width=40, height=24, unit='cm')


def summr(csv):
    nm = os.path.basename(csv).split('.')
    drnm = os.path.dirname(csv)
    a = pd.read_csv(csv)
    robjects.r('''
    summr <- function(z) {
    foo <- z %>% group_by(plt_nm, condt) %>%
    dplyr::summarise(mean_area = mean(area), median_area = median(area), sd_area = sd(area), mean_zneg = mean(zneg), sd_zneg = sd(zneg), mean_zpos = mean(zpos), sd_zpos = sd(zpos))
    }
    ''')

    r_summr = robjects.globalenv['summr']
    raz = r_summr(a)
    r.data('raz')

    pd_df = pandas2ri.ri2py_dataframe(raz)
    pd_df.to_csv((drnm + '/' + nm[0] + '_sumfile_BY-COL.csv'), index=False)

def summr_ov_cd(csv):
    nm = os.path.basename(csv).split('.')
    drnm = os.path.dirname(csv)
    a = pd.read_csv(csv)
    robjects.r('''
    summr_rp <- function(z) {
    foo <- z %>% group_by(condt) %>%
    dplyr::summarise(mean_area = mean(area), median_area = median(area), sd_area = sd(area), mean_zneg = mean(zneg), sd_zneg = sd(zneg), mean_zpos = mean(zpos), sd_zpos = sd(zpos))
    }
    ''')

    r_summr_rp = robjects.globalenv['summr_rp']
    raz = r_summr_rp(a)
    r.data('raz')

    pd_df = pandas2ri.ri2py_dataframe(raz)
    pd_df.to_csv((drnm + '/' + nm[0] + '_sum_ov_condt_BY-COL.csv'), index=False)

## plots all

def pltala(a):
    a0 = pd.read_csv(a)

    robjects.r('''
        pltala <- function(z) {
  p <- ggplot(z, aes(x = well, y = area)) +
  geom_point(aes(color = condt, shape = toString(plt_nm)),
             alpha = 0.6,
             size = 3) +
  scale_y_continuous(labels = scales::comma) +
  labs(title = 'All Raw Area',
       y = "Area (AU)",
       x = "well",
       color = "Condition",
       shape = "Condition") +
  theme(axis.title.x = element_blank(),
        axis.ticks.x = element_blank(),
        axis.text.x = element_blank(),
        panel.grid.major.x = element_blank())
    a = ggplotly(p)
    htmlwidgets::saveWidget(a, '../final/all_raw_BY-COL.html')
        }
            ''')

    r_pltala = robjects.globalenv['pltala']
    rez = r_pltala(a0)

## Plots all on zscore

def pltalz(a):
    a0 = pd.read_csv(a)

    robjects.r('''
        pltalz <- function(z) {
  p <- ggplot(z, aes(x = well, y = zneg)) +
  geom_point(aes(color = condt, shape = toString(rep)), alpha = 0.6, size = 3) + facet_grid(~plt_nm) +
  scale_y_continuous(labels = scales::comma) +
  labs(title = "All z-score",
       y = "Zscore",
       x = "Well",
       color = "condt",
       shape = "rep") +
  theme(axis.title.x = element_blank(),
        axis.ticks.x = element_blank(),
        axis.text.x = element_blank(),
        panel.grid.major.x = element_blank())
    a = ggplotly(p)
    htmlwidgets::saveWidget(a, '../final/all_z-score_BY-COL.html')
        }
            ''')

    r_pltalz = robjects.globalenv['pltalz']
    rez = r_pltalz(a0)

## plots all hits w mean lines
def pltalmpl(a, b):
    a0 = pd.read_csv(a)

    robjects.r('''
plot.meapl <- function(t, u) {
  z <- t %>%
    group_by(plt_nm) %>%
    filter(condt == "+ctrl") %>%
    summarise(average = mean(zneg))
  exp <- t %>%
    filter(condt == "exp") %>%
    filter(zneg > u)
  y <- ggplot(data = exp, aes(x = well, y = zneg)) +
    geom_point(data = exp, aes(color = plt_nm)) +
    geom_hline(data = z, aes(yintercept = average), linetype="dashed") +
    facet_grid(~plt_nm) +
    scale_y_continuous(labels = scales::comma) +
    labs(title = "hits w/avg z-score of +ctrls",
         y = "zscore rel. to -ctrl",
         x = "well") +
    theme(axis.text.x = element_blank(),
          axis.ticks.x = element_blank())
    bb <- ggplotly(y + theme(legend.position="none"))
    htmlwidgets::saveWidget(bb, '../final/all_hits_z-pos-mean_BY-COL.html')
        }
            ''')

    r_pltalmpl = robjects.globalenv['plot.meapl']
    # rez =
    r_pltalmpl(a0, b)

## plots all tox w mean lines
def pltalmnl(a):
    a0 = pd.read_csv(a)

    robjects.r('''
plot.meanl <- function(t) {
  z <- t %>%
    group_by(plt_nm) %>%
    filter(condt == "-ctrl") %>%
    summarise(average = mean(zneg))
  exp <- t %>%
    filter(condt == "exp") %>%
    filter(zneg < -2)
  y <- ggplot(data = exp, aes(x = well, y = zneg)) +
    geom_point(data = exp, aes(color = plt_nm)) +
    geom_hline(data = z, aes(yintercept = average), linetype="dashed") +
    facet_grid(~plt_nm) +
    scale_y_continuous(labels = scales::comma) +
    labs(title = "toxs w/avg z-score of +ctrls",
         y = "zscore rel. to -ctrl",
         x = "well") +
    theme(axis.text.x = element_blank(),
          axis.ticks.x = element_blank())
    bb <- ggplotly(y + theme(legend.position="none"))
    htmlwidgets::saveWidget(bb, '../final/all_hits_z-neg-mean_BY-COL.html')
        }
            ''')

    r_pltalmnl = robjects.globalenv['plot.meanl']
    # rez =
    r_pltalmnl(a0)

## Plots all on zscore

def pltalz(a):
    a0 = pd.read_csv(a)

    robjects.r('''
        pltalz <- function(z) {
  p <- ggplot(z, aes(x = well, y = zneg)) +
  geom_point(aes(color = condt, shape = condt), alpha = 0.6, size = 3) + facet_grid(~plt_nm) +
  scale_y_continuous(labels = scales::comma) +
  labs(title = "All z-score",
       y = "Zscore",
       x = "Well",
       color = "condt") +
  theme(axis.ticks.x = element_blank(),
        axis.text.x = element_blank(),
        panel.grid.major.x = element_blank())
    a = ggplotly(p)
    htmlwidgets::saveWidget(a, '../final/all_z-score_BY-COL.html')
        }
            ''')

    r_pltalz = robjects.globalenv['pltalz']
    rez = r_pltalz(a0)

# This will give you a new dataframe with a new column that shows the mean of all the other columns
# col = df.loc[: , "salary_1":"salary_3"]
# df['salary_mean'] = col.mean(axis=1)
