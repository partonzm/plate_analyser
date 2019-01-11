Attributions:
  License - GNU v3
  Funding - Perlara, PBC
  Python scripting - Zach Parton
  R scripting - Hillary Tsang, Zach Parton
  Director - Sangeetha Iyer

************************************* Work flow (last: 31Aug18) *************************************

To note: This script has been written by and for PERLARA PBC to analyze plates coming off of the modularscience custom-built 384-well plate imager (meant for C. elegans). It provides a set of modules which (when more fully functionalized) can be ported to other high-throughput screening projects.

Ensure file names are correct!!! 

ORGANISM_DISEASE_EXP#_PLATENAME*_Img-Cond_Date_wells.csv* - NB all between ** is autopopulated from worm imager machine

Organize plates to be analyzed by replicate:

data/
  rep1/
    plate1
    plate2
    ...
    platen
  rep2/
    plate1
    plate2
    ...
    platen
  ...
  repn
    plate1
    plate2
    ...
    platen

(NB as well that the above is agnostic to how many reps or plates are per rep: however, hits will only be pulled into the all_excl_all_hits_final.csv is they appear in all replicates present)

Run "python3 wm_az.py"

Annotate all_hits_final.csv & all_tox_final.csv wth a column named "status" and the following distinctions:

## enviromental variables
zhlim = X ## hit limit
ztlim = Y ## tox limit
zxlim = Z ## ctrl exclusion

  HIT  - zneg score >X & visual confirmation of performance near positive controls
  wkht - zneg score >X & visual confirmation of performance better than negative controls
  arht - zneg score >X & visual confirmation of imaging artifacts
  N/A - not of interest
  artx - zneg score < -Y & visual confirmation of imaging artifacts (or lack thereof)
  wktx - zneg score < -Y & visual confirmation of performance around negative controls
  TOX - zneg score < -Y & visual confirmation of performance worse than negative controls

Run the "python3 cdd.py"

REQUIRED BEFORE NEXT ANALYSIS : rename "final" folder in root dir to general experiment name with specific processing conditions


************************************* File Key (last: 3July18) *************************************

## enviromental variables
zhlim = X ## hit limit
ztlim = Y ## tox limit
zxlim = Z ## ctrl exclusion

all.csv : all wells with original z-negative scores (before auto exclusion)

all_excl.csv : all wells with z-negative scores calc (after exclusion of controls using zxlim to define tails)

all_excl_all_hits.csv : all wells with a "zneg" > zhlim (hits)
all_excl_all_hits_final.csv : all hits occuring across all reps

all_excl_all_tox.csv : all wells with a "zneg" < ztlim (tox)
all_excl_all_hits_final.csv : all tox occuring across all reps

all_excl_repX_O.csv : all (O = tox or hits) in replicate X

all_Outliers: all ctrl wells with abs(zscore) > zxlim

all_*_sum_condt.cvs : summary file by condition across reps (* by excl or raw)
all_*_sumfile.csv : all summary (ea plate) (* by excl or raw)
all_*_sum_plate.csv : summary file by plates across reps (* by excl or raw)


Graphs:
repX_raw.png : raw area box plots per plate per rep
repX_zscore.png : zscore box plots per plate per rep (to gain understanding of seperation)
test_all-z.html : interactive scatter off z-score (after exclusion)
test_raw.html : interactive scatter off raw area (before exclusion)


TO NOTE:
All files with _excl have a recalculated z-score (neg & pos) after exclusion

************************************* az_code-outline (last: 30Aug18) *************************************

General Overview (Steps):
  1) Aggregate data
  2) Calculate Z-scores (1)
  3) Do exclusion
  4) recalculate z-scores (2)
  5) Call HITs/TOX
  6) Plot
  
General project structure:
  wm_az-vX/ # X name of version
    general docs - README, TODO, LICENSE
    setup.py # not implemented yet
    requirements.txt
    /data   # folder for putting in rep folders containing plate data
        rep1/
            plate1...
            ...
            platen...
        rep2/
        ...
        repn/
        
    wm_az/
        data/
        bin/    #stores all the modules
        wm_az.py - script for processing plate files in 

Definitions:
  Z-score :: "Simply put, a z-score is the number of standard deviations from the mean a data point is." (statisticshowto.com) This is representative (normalized statistic) of how the experimental conditions perform relative to normal or untreated-affected animals.

  Positive control (+ctrl) :: unaffected animals that perform at a "normal" level (no drugs or experimental conditions)

  Negative control (-ctrl) ::  affected animals without test compounds (experimental conditions) that will perform worse than normal.

  dynamic range :: (not mentioned elsewhere, but useful for conceptualizing) the degree by which the performance of the positive and negative controls differ (how "real" are the effects of the affect).

  HIT :: Compound which performed better than the zplim relative to negative controls

  TOX :: Compound which performed worse than the znlim relative to negative controls
  
0) Opening

  0.1) Define Variables (See usage below)
  Rationale: We will need different limits for different experiments. This should be moved to a .hjson or similar config file
  
    zplim - defines z-score for HITs categorization
    znlim - defines z-score for TOX categorization
    zxlim - defines exclusion limits

  0.2) Shuttle data around
  Rationale: data is moved to a /final folder for ease of use and segregating processed vs unprocessed data
    
    makes new directory
        os.mkdir('../final')
        
    moves all data into final/
        shutil.move('../data', '../final/') 
    
    remakes top level data directory for future processing
        os.mkdir('../data') 


1) Aggregate data

  1.0) get glob
  Rationale: data processing should be done on all relevant and only on relevant files
    aa = glob.glob('../final/data/*/*.csv')

  1.1) Clean data
  Rationale: some data needs to be reformatted
  
    1.1.1) Rename data files by plate name - this relies on the data to be named correctly with the 3rd part of the name (divided by "_") to become the csv file name.
        clnr.repsplit(aa)

    1.1.2) get new glob (because of renaming)
        bb = glob.glob('../final/data/*/*.csv')

    1.1.3) inject source file - imported to extract plate name column could be done earlier with the original glob. dropped later.
        clnr.pltnmij(bb)

    1.1.4) inject plate name as column - uses source name from above
        clnr.pltnmr(bb)

    1.1.5) inject replicate into csv - uses source directory
        clnr.repij(bb)

    1.1.6) cleans up - renames a couple columns and drops some uneeded ones
        clnr.clnrr(bb)

    1.2) Split well letter (row) from number (column)
    Rationale: ease of annoatation
        clnr.idxr(bb)
  
    1.3) Annotate data - 
    Rationale: annotates either positive controls (+ctrl), negative controls (-ctrl), and experimental (exp) wells - should be ported to a function where these annotation parameters can be specified in a config file.
        clnr.annt(bb)

2) Calculate Z-scores (1)

  Rationale: Calculate z-score per-plate relative to positive and negative controls. needed to EXCLUDE outliers from controls, in order to confirm effects and not have distorted averages & to judge whether an experimental well is a HIT or TOX
  
    2.1) Calculate z-score of every well relative to negative controls
        rscrps.zscrn(bb)
    2.2) Calculate z-score of every well relative to positive controls
        rscrps.zscrp(bb)
  
3) Cleanup #2

    3.1) Cleans up data - drops additional columns and reorders the csv more coherently
        clnr.clnr2(bb)
    
    3.2) Aggregate into single csv - the "all" - straight forward
        clnr.mrgr(bb)


3) Exclusion
  Rationale: R-script based function to exclude outliers from the control groups, based on their respective z-scores. If a control performs too far away from the average, we dont want to use it to determine the status of an experimental well. It will skew the data away from "true"
    mats2.ex('../final/all.csv', zxlim) - nb only on all.csv, we don't want to lose these wells from the original data files - appends "_excl"
  
4) recalculate z-scores (2)

  Without outlier controls, calculate new z-scores relative to positive and negative controls (only negative used past this point)
  
  4.1) get new glob for all "_excl"|exclusion-done files
    dd = glob.glob('../final/*_excl.csv')

  4.2) re-calc zscores on glob (as above)
    rscrps.zscrn(dd)
    rscrps.zscrp(dd)

5) Call HITs/TOX
    Rationale: 
    If an experimental well (a particular compound) has a z-score relative to negative controls ABOVE the zplim, we are interested in it as it significantly has brought the animals closer to the positive control condition. We call this a HIT
    If an experimental well (a particular compound) has a z-score relative to the negative controls BELOW the znlim, we are interested in it as well, as it has significantly worsened the animals performance relative to the negative controls (i.e. is toxic). We call this a TOX
    
    5.1) pull all experimental (exp) wells that score above the zplim
        mats2.hits('../final/all_excl.csv', zplim)
        
    5.2) pull all experimental (exp) wells that score below the znlim
        mats2.tox('../final/all_excl.csv', znlim)
        
    We are particularly interested in experimental conditions that performed well across the board (replicates):
    
    5.3) pull all HITs that appear in all replicates and record them once:
        mats2.countr('../final/all_excl_all_hits.csv')
        
    5.3) pull all TOXs that appear in all replicates and record them once:
        mats2.countr('../final/all_excl_all_tox.csv')

6) Finishing

    6.1) load in final finals of interest:
        a = '../final/all_excl.csv'
        b = '../final/all.csv'

    6.2) summarize the data
    Rationale: certain metrics will be useful for commenting on the validity of our studies. These "summr" modules are r-native summarizing functions. This functionality could possibly collapsed into a single module or complex function. Still very rough, but useful.
        6.2.1) summarize data on which exclusion had been performed (excl)
            rscrps.summr(a)
        6.2.2) summarize data on which exclusion had NOT been performed (raw)
            rscrps.summr(b)
        6.2.3) summarize by plate (excl & raw)
            rscrps.summr_pl(a)
            rscrps.summr_pl(b)
        6.2.3) summarize by replicate (excl & raw)
            rscrps.summr_rp(a)
            rscrps.summr_rp(b)        
 
    6.3) Plot:
    Rationale: need to vizualize the data! These scripts use r functions to plot the data and save it. the pltal_ functions save interactive graphs (native r functionality)
    
       6.3.1) box & whisker plot of controls (excl & raw)
            rscrps.ctrlbxa(b)
            rscrps.ctrlbxz(a)

       6.3.2) plots raw areas 
            rscrps.pltala(b)
            
       6.3.3) plots znegative scores (after excl)
            rscrps.pltalz(a)
       
       6.3.4) plots controls only with their respective mean lines (to check the range of performance after exclusion)
            rscrps.pltalmpl(b)
            rscrps.pltalmnl(b)


    6.4) Export metadata
    Rationale: we should have a quick reference for how the plates were run - could just be a (simplified) copy of a .hjson file once that is implemented.
    
    a = 'hit limit = ' + str(zplim)
    b = 'tox limit = ' + str(znlim)
    c = 'excl limit = ' + str(zxlim)
    d = 'Analysis done at: ' + str(datetime.datetime.now())
    f = open('../final/meta.txt', 'w')
    f.write(a + '\n' + b + '\n' + c + '\n' + d)

