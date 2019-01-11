#!/usr/bin/env python
# -*- coding: utf-8 -*-

# """CLEEAN FOR PRESENT!"""

## creates a pretty b/w graph for presenting

## __Import__
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
htmlwidgets = importr('htmlwidgets')

# forcats = importr('forcats')
dt = importr('data.table')

def plthit(o):

    robjects.r('''
        plthit <- function(z) {
  a <- read.csv(z)
  aa <- a %>% filter(condt == "exp")
  hits <- a %>% filter(status == "HIT")
  bb <- mean((a %>% filter(condt == "-ctrl"))$zneg)
  dd <- mean((a %>% filter(condt == "+ctrl"))$zneg)

  p <- ggplot(aa, aes(x = well, y = zneg)) +
      geom_point(aes(shape = rep), color = "dark grey", alpha = 0.2, size = 3) + facet_grid(~plt_nm) +
      scale_y_continuous(labels = scales::comma) +
      labs(title = "All z-score",
           y = "Zscore",
           x = "Well") +
      theme(axis.title.x = element_blank(),
            axis.ticks.x = element_blank(),
            axis.text.x = element_blank(),
            panel.grid.major.x = element_blank()) +
      geom_hline(yintercept = bb) + geom_hline(yintercept = dd) +
      geom_point(data = hits, aes(x = well, y = zneg), size = 3) #+ scale_color_brewer(palette="Paired")

  a =ggplotly(p)
  htmlwidgets::saveWidget(a, 'all_hits.html')
        }
            ''')
    r_plthit = robjects.globalenv['plthit']
    ryz = r_plthit(o)
