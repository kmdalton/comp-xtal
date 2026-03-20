---
id: basic-programs-tasks
title: Basic: CCTBX.XFEL Programs and Tasks
---

1. Defining Trial (i.e. Indexing parameters) 
Go to the “Trials” page of the GUI. 
This is a somewhat peculiar part of how the GUI is organized. When creating a trial, what you put in the big textbox is actually parameters for the Indexing task. However, all the other tasks are defined under Datasets (see step 2). 
The format/grammar of the content is the same as the phil file, which stands for Python 
Hierarchical Input Language (a kind of format used for cctbx and phenix programs): <https://cci.lbl.gov/docs/cctbx/doc_low_phil/> 
Under the hood, the Indexing task is performed by calling the program dials.stills_process. If you don’t know what parameters are accepted by this program to put in the textbox, you can use dials.stills_process -ca 2 -e 10  
Similar command works for other cctbx/dials programs if you want to learn more about the parameters, and the flags specify the expert (verbose) level of the help messages. 
An example input looks like this: 
dispatch { 
  hit_finder { 
    minimum_number_of_reflections = 16 
  } 
} 
spotfinder { 
  filter { 
    min_spot_size = 2 
    max_spot_size = 100 
  } 
  threshold { 
    algorithm=dispersion dispersion { 
          gain = 1 
          kernel_size = 1 1 
          global_threshold = 10 
    } 
  } 
} 
indexing { 
  stills.reflection_subsampling.enable=True

known_symmetry { 
    space_group = P 1 21 1 
    unit_cell = 87.970 52.420 95.650 90 95.609 90 
  } 
  refinement_protocol { 
    d_min_start = 2 
  } 
  multiple_lattice_search { 
    max_lattices = 3 
  } 
}

Remember to check space group and unit cell information here (and make new trials if necessary) if you have samples with distint values. 
    During real-time processing, it could be helpful to add the line integrate = False within the dispatch block (above hit_finder) to speed up the indexing results. However, remember to either re-run (by making another trial) without this flag or perform ensemble refinement to make sure you can eventually do scaling and merging (See Section 3. Within a 
Dataset, Defining Task) 
Within a trial, define Run Group 
- You need to specify the start and end (inclusive) runs. For real-time processing, “Auto add run” can be helpful, but you need to remember terminate it by specifying the end run one sample is changed. 
- A path to .expt file that specifies the geometry (see step a below) at the top textbox.  
- Under the second large text box “Extra XTC format parameters”, for psana2, you need to put the line “mode=psana2_idx”.  
- Specify the detector name. If you don’t know exactly the format, the detnames program from psana is helpful (see the Debug chapter). 
- Specify binning, if any 
- Put in the spectrum_eV_per_pixel and spectrum_ev_offset values if you have that (see the 
Photon energy calibration chapter). You can either manually input them, or if you have saved the .phil from photon energy calibration, or use the “Import PHIL” button to populate the values from the file for you. 
- Load the pixel mask (see step b). If you don’t know how to make mask, see the corresponding chapter.

a. For each run group specify the geometry file 
For the example experiment we look at, the detector calibration was performed using 
LaB6. The experiment file can be found here:

/sdf/data/lcls/ds/mfx/mfx100904224/results/common/geom/LaB6_r0005_louisupdate d.expt 
This will be input.reference_geometry in the run block settings 
The .expt file will overwrite the values in the text boxes below for “Beam: X Y DetZ” 
b. For each run group load pixel mask 
For the summers experiment a mask can be found here: 
/sdf/data/lcls/ds/mfx/mfx100904224/results/common/pixels.mask 
This can be used in the following

c. Extra XTC format parameters 
Other than specifying mode for psana2, if there are any issues of the XTC files, this textbox is likely where you need to modify, such as specifying spectrum address, putting a wavelength fallback value when eBeam is missing etc. Content in this textbox will be part of the data.loc file that enables retrieving and viewing the images.

d. Check this trial as the active trial, and uncheck other if you previously have other processing. 
2. Defining Datasets  
Go to the “Datasets” page of the GUI. 
Refer to “Tagging runs” in the previous chapter step 3 “Populating runs” if you have no clue about tags.  
Depending on how you tag the runs, select if you want the intersection or the union of the tags to process a dataset. Intersection makes sense if say you have one tag of mixing time and another tag for temperature. Union makes sense if you want to combine runs that are similar (e.g. tagged by different delivery speed but otherwise the same sample). 
Not all runs defined by the tags you choose will be processed – only runs within the run groups of the trial will be used to look at tags. For example, run 1-40 are all tagged as apo, but your run group under the trial is defined as run 20-40, then the apo dataset will only process run 20-40. See below on task definition to see where trial comes in.  
The name of the dataset will become the name of the folder for the Merging task.  
    Do NOT contain space or weird characters in the dataset name, as merging can fail. 
Use a single word (linked by underscore is fine). 
Check this dataset as the active dataset, and uncheck other if you previously have other processing. 
3. Within a Dataset, Defining Tasks 
Each task has to be associated with a specific trial. Under a dataset, click “New Task” to add a task and specify the trial and the parameters (PHIL format) for that task. ”Typically, you would have the following 4 tasks to run for a dataset:

The tasks you define are chained in the listed order, such that for a particular run, a local task (e.g. scaling, see explanation below) won’t run until the previous local task finishes. 
Ensemble refinement is an optional task, so you could just chain a scaling task right after the indexing task.   
    You might notice that in practice, after you define the trial and run groups, with the 
“Auto submit jobs” button on, indexing jobs can be automatically submitted for those runs, even if you haven’t defined the Indexing task. 
    That said, you must define the Indexing task explicitly in the Dataset and chain the other tasks (such as shown in the screenshot above) in order to run the other tasks. For example, you cannot leave only Scaling and Merging tasks there, even if you have already got Indexing and Ensemble refinement results from previous processing. 
    Technically you can chain Indexing task directly to Scaling task. However, make sure you did NOT set integrate=False for Indexing (which, remember, is set when you define the trial and cannot be edited).

Task Output Folder Structures 
Local task 
Indexing, ensemble refinement, and scaling are all considered local task, meaning the task is performed at the level of each run, and the outputs are organized under each run. A 
typical run folder structure (relative to experiment folder path) is this: 
r0023/002_rg015 
Which means the ouput is for run 23 processed from indexing parameters in trial 2 and other information (e.g. geometry and pixel mask and energy calibration) associated with run group 15. 
The non-indexing local task has its own output folder named by the task id its assigned by the GUI, e.g. r0023/002_rg015/task009 
Global task  
Merging, however, is a global task as it is performed across runs. The output folder is named by the dataset name, and lives in the experiment folder where each run folder lives. 
This task will be run for many versions, as the previous local task (scaling) finishes for more and more runs. See the “Outputs” subsection under the “Merging” section below for more details.

Indexing 
See step 1 for trial definition. You don’t need to put any parameters here. 
Outputs: 
Within the run folder, you would have a data.loc file, out folder, stdout folder, a params_1.phil file, and slurm job submission script submit.sh and its wrapper submit_submit.sh. 
The out folder contains the .expt and .refl outputs. One idx-{number}_refined.expt file does NOT necessarily mean 1 image – it could contain multiple images:

The “single_file_indices” tells you the actual index of the image. In other words, if you are viewing all images (including non-hit) of the entire run using dials.image_viewer data.loc load_models=False, you can jump to view the same image using this index 
(+1, apparently 0-indexed). 
To just view some example of indexed images, you could do dials.image_viewer idx-
{whatevernumber}_*.{expt,refl} load_models=False 
Errors of the job would end up in the stdout folder although it is very hard to debug 
(especially mpi related) errors based on messages there. I usually only look at the err.out file there. 
The parameters you put under trial definition would end up in params_1.phil. 
“Extra XTC format parameters” would end up in data.loc, which used by the GUI to talk to psana and get images data. 
See the chapter “Intermediate: Indexing result improvement” for more details on checking the indexing statistics and strategies for improvement.

Ensemble refinement 
Refines the geometry, unit cell, etc. and performs integration.  
Example inputs combine_experiments.clustering.use=False reintegration.integration.debug.output = True reintegration.integration.debug.separate_files = False reintegration.integration.mp.nproc = 32 
reintegration.integration.summation.detector_gain = 0.46

You may want to change the detector _gain in the last line depending on the type of detector (e.g. 1 used for Epix10ka2M).

Outputs: 
Within the task output folder (e.g. r0023/002_rg015/task009),  it has another folder like combine_experiments_t002, where t002 means trial 2. Within this folder, you two folders final_extracted and intermediates. The integration results (.expt and .refl files) as well as log files are in the intermediates. 
Scaling 
Scaling and Merging both use cctbx.xfel.merge program, and it’s the dispatcher list that decides what processing is actually performed. An example phil parameters for scaling is attached below. As you can see, “scaling” is there, but it really is just one of many steps needed to perform for the Scaling task. 
Example inputs dispatch.step_list=input balance model_scaling modify filter errors_premerge scale postrefine statistics_unitcell statistics_beam model_statistics statistics_resolution input.parallel_file_load.method=uniform filter.outlier.min_corr=-1 
filter.algorithm=unit_cell filter.unit_cell.value.relative_length_tolerance=0.01 
select.algorithm=significance_filter select.significance_filter.sigma=0.1 
#select.significance_filter.min_ct=200 
#select.significance_filter.max_ct=300 
scaling.model=/sdf/data/lcls/ds/mfx/mfxl1008021/results/common/models/
L10080_no_mix_rsich_refine_6.pdb scaling.resolution_scalar=0.96 
merging.d_min=1.2

merging.merge_anomalous=True postrefinement.enable=True statistics.n_bins=20 
output.save_experiments_and_reflections=True 
Outputs: 
The task output folder is structured very similar to the indexing output folder (one level up of this task output folder), except that there is not data.loc file here. 
Merging 
Example inputs dispatch.step_list=input model_scaling statistics_unitcell statistics_beam model_statistics statistics_resolution group errors_merge statistics_intensity merge statistics_intensity_cxi publish input.parallel_file_load.method=uniform scaling.model=/sdf/data/lcls/ds/mfx/mfxl1008021/results/common/models/
rsich_high_dmso_150ms_mixing.pdb scaling.resolution_scalar=0.96 
statistics.n_bins=20 
merging.d_min=1.28 
merging.merge_anomalous=True merging.error.model=mm24 
To upload merged .mtz files into google drive, refer to this instruction to set up 
(https://github.com/cctbx/cctbx_project/tree/master/xfel/merging/application/publish), and add two more lines in the inputs: 
publish.drive.credential_file= 
publish.drive.shared_folder_id=

Additional notes 
   If you don’t specify the google drive related parameters to publish mtz files but you have publish in your dispatch.step_list, the merging job will finish with a status “EXIT” 
which normally indicates something went wrong wit the job, but here it could be fine. You can check the err.log the output folder to confirm it is this type of error that led to EXIT, and you should still have all the other proper output files. 
    If you are looking at some old processing data, you might see phil parameters like merging.error.model=ev11 
merging.error.ev11.algorithm= 
This was prototype (deprecated) code and is transitioned to mm24 now.

Outputs: 
Within the output folder (named after the dataset, lives under the experimental folder), there are many versions as more runs coming in. For final result, you want to look at the folder with the largest version number. Within this folder, the key files are: 
- {dataset_name}_v{version_number}_main.log: contains merging stats 
- {dataset_name}_v{version_number}_all.mtz: overall merged output 
- {dataset_name}_merging{task_id}_v{version_number}_params.phil: your input parameters 
- {dataset_name}_merging{task_id}_v{version_number}_submit.sh 
There are also a lot of other logging files, including log.out and err.out, and wrapper submit script for slurm.  
For quick triage I would mainly focus on the tables shown below in the ...main.log file. The tables for all (rather than for odd/even) are closer to the end of the file. I would look at obs_multi > 10, CC1/2 > 0.3, and other metrics to decide resolution and if any pathology.

Quick Workflow Checklist 
1. Connect via FastX 
2. ssh -Y into S3DF 
3. Source env: 
 source /sdf/group/lcls/ds/tools/cctbx/setup.sh 
4. Copy .phil settings 
5. Start GUI → enter experiment info 
6. Configure DB credentials 
7. Set options + advanced settings 
8. Start processing (watch new runs or manual selection) 
9. Geometry calibration and energy calibration, in either order

10. Make/load Pixel Mask 
11. Define trial, run groups if not already 
12. Define dataset 
13. Start an indexing task (or more)

<!-- handbook-pdf-figures-begin -->

### Figures (from PDF)

![PDF p.16 fig.1](images/basic-programs-tasks_p16_01.png)

![PDF p.16 fig.2](images/basic-programs-tasks_p16_02.png)

![PDF p.17 fig.3](images/basic-programs-tasks_p17_03.jpg)

![PDF p.19 fig.4](images/basic-programs-tasks_p19_04.jpg)

![PDF p.21 fig.5](images/basic-programs-tasks_p21_05.png)

![PDF p.25 fig.6](images/basic-programs-tasks_p25_06.png)

![PDF p.25 fig.7](images/basic-programs-tasks_p25_07.png)

<!-- handbook-pdf-figures-end -->

