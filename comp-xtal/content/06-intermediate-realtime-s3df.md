---
id: intermediate-realtime-s3df
title: Intermediate: Prepare for real-time usage during beamtime (S3DF)
---

Intermediate: Prepare for real-time usage during beamtime (S3DF) 
Before the beamtime 
General 
- Check that the experiment folder has been set up on S3DF and visible on eLog 
- Collect Dark runs (test takepeds/makepeds) 
- Collect calibrant data and run BayFAI (during commissioning) 
Note on BayFAI / geometry – 2026/02 
See LUTE documention on how to set up and run BayFAI to estimate geometry: 
https://slac-lcls.github.io/lute/dev/usage/tasks/bayfai/bayfai/ 
As of 2026/02, this involves following the instructions linked above in the experiment folder. After the set up, you should see the BayFAI workflow auto-populated on elog --> 
Workflow --> Definitions, and you can adjust it appropriately. For example, you want to change the Trigger to MANUAL rather than the end of each run, and maybe adjust slurm arguments like --ntasks as needed. 
Database 
Make sure the users have requested to set up MariaDB on their form to use cctbx.xfel GUI. 
If this step is missing, you need to email pcds-datamgt-I to set it up. 
If you try to launch the GUI and see the following error, then DB is not set up properly yet.

You can also verify this with mysql command: 
mysql -h 172.24.5.182 -u <experiment> <experiment> -p 
See the Debugging chapter regarding Database for more mysql commands and info. 
GUI readiness 
Some test runs (energy calibration) should be done before the beamtime to test GUI basic functionality. 
- Can you successfully launch the GUI? Check that remote access works, and sourcing the cctbx environment works. 
- Can the GUI access MariaDB and you see the runs when clicking “Watch for new runs”? 
- Can you do some fake jobs just to see if they can even be submitted/run? Like averaging a run and visualize the averaged image? 
Analysis info 
- Unit cell and space group, and a reference PDB file from users 
- A template of phil parameters (at least for the Indexing task/trial definition), might be from users or from a recent beamtime 
- Optionally a reference geometry .expt file, potentially from a recent beamtime, if not using BayFAI 
- Optionally a reference mask file, potentially from a recent beamtime 
During the beamtime 
The main question to answer during beamtime is have enough data been collected to move on. Ideally, you want to proceed all the way to merged results and look at the stats there. In practice, many difficulties can come up, and a quick ballpark can come from the number of indexed images. 
Make initial files for indexing 
If you don’t have a geometry file yet, start with averaging a run and create one.  
If you don’t have a mask yet, start with an averaged run and make one. 
It is unlikely that your initial files and phil parameters are good enough. Typically then you need to perform energy calibration, refine the geometry, update the mask, and maybe even explore the phil parameters for spot finding etc. This means that indexing (different trials) and ensemble refinement tasks could be processed many times in slight variations, just like how you would have run the GUI for offline reprocessing.

Hit/indexing progress 
You want to monitor “Run Stats” and “Unit Cell” tabs to look the rate and the number of successfully indexed images. Some users might have a rough estimate of how many indexed crystals they need. 
You might find the following tricks helpful to speed up the processing: 
- Set up persistent tag to automatically tag incoming runs (but remember to change it when sample changes). 
- Set integrate=False when defining the Trial to perform just indexing without integration. Remember to get rid of this or perform ensemble refinement to eventually do scaling/merging. 
Merging progress 
If things are going well and we are beyond indexing and integration, next we can look at scaling and merging. You want to look at the “Merging stats” tab: 
The “Active only” refers to the dataset, and you can untick it or not. Leave the Dataset version as “All” and you should see how the statistics evolve over the versions (the version number increases as more images come in).  
   Do NOT select a particular version of the dataset. The plotting will fail (the sentinel 
“Merging Stats” on the bottom right turns red) and you might need to switch to other tabs and then come back to refresh the GUI out of a failed status, or relaunch the GUI. 
    Note that it can take a while to plot the image, and the main way to tell if the plotting is hanging/stuck or not is to look at the sentinel. If after a few seconds of no update and the sentinel hasn’t changed to yellow (working) (or it has changed to red), it might be stuck.

You want to see the metrics increase monotonically and plateau as you collect sufficient data. Make sure to not lump together different samples under a dataset as that could mess up the stats trajectories.  
The purpose of this tab is to gauge if more data need to be collected. To see a more comprehensive and details set of merging statistics, you should go to the ...main.log file in the merging output folder.

<!-- handbook-pdf-figures-begin -->

### Figures (from PDF)

![PDF p.27 fig.1](images/intermediate-realtime-s3df_p27_01.png)

![PDF p.30 fig.2](images/intermediate-realtime-s3df_p30_02.png)

<!-- handbook-pdf-figures-end -->

