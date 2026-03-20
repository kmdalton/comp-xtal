---
id: intermediate-geometry-refinement
title: Intermediate: Geometry Refinement
---

cctbx/dials understands the geometry through psana. If BayFAI was used to estimate detector distance, it will push the result to a database such that psana2 Datasource can retrieve information from it, and this is how cctbx will understand the initial geometry. For psana1, this depends on the file written by BayFAI to the calib folder of the experiment: 
/sdf/data/lcls/ds/mfx/{experimentname}/calib. This file is still written for psana2 BayFAI 
but is just for logging purpose as the database is the way to communicate with cctbx now. 
Without BayFAI, psana use the default metrology data. 
Obtaining an initial geometry .expt file 
Average a run 
If cctbx can retrieve images and geometry from psana properly, you would first click 
“Average” for the calibrant run to make powder:

Under the hood, averaging a run uses geometry from psana, which could come from 
BayFAI or default metrology. 
The status of the average job is not checked in GUI under jobs, but actually in the terminal like your regular slurm job submission.  
Once averaging is done, go to the output folder, should be output path like:  
/sdf/data/lcls/ds/mfx/{experiment_name}/results/{experiment_tag}/averages/000 
If you see more folders like 000, 001, ... these are different versions of averaging done for this run. Within a version folder, you should have data.loc, submit.sh, submit_submit.sh 
(wrapper submit script), and the out and stdout folders. In the out folder,  you should have max.cbf, std.cbf, and avg.cbf. I find it easier to work with max.cbf for geometry stuff, and std.cbf for masking.

Generate an initial .expt file 
In the terminal at the out folder:  
dials.import max.cbf wavelength=1.4443 
By default it generates a file named imported.expt.

Visualize in dials.image_viewer the geometry fit 
Launch image: dials.image_viewer imported.expt 
If the calibrant is LaB6 rather than Agbe, add the following to the command above: 
unit_cell=4.15,4.15,4.15,90,90,90 
After you have the image viewer pop up, click “Actions” --> “Show unit cell tool”, which would pop up another window.

1. Lower the “Highest resolution for ring display” and hit enter to show the rings. In this case, 1.7 is a good value to display rings to the edge of the image.

2. If the red rings are a bit off with respect to the actual powder signals, you can explore some manual fitting here through “Detector Distance”, “Center fast” (x-axis, positive points to right), “Center slow” (y-axis, positive points down).  
Notes and tips: 
- The “Detector Distance” is auto-populated through the .expt file from psana geometry, but in practice we have seen some discrepancy between the values. 
Generally speaking, as long as the fit looks good, you can proceed and give indexing a try. See “Understand the detector distance number” section below for more details. 
- If you manually refine the distance or the X/Y position in the “Unit cell tool” window, it won’t be saved to the .expt file. You would need to edit the values in the corresponding section in the .expt file. See “Understand the detector distance number” and “Modify beam X/Y (Center fast/slow)” sections below for more details. 
- If you mis-enter something of the wrong format, the image viewer could just crash/freeze, you would have to start over. 
Understand the detector distance number 
    As of 2025/11, there is some weird discrepancy between the value in the .expt file and the value populated in dials.image_viewer. We don’t fully understand why, but at least for mfx100904224 run 5 it seems okay enough to have some indexing results and refine geometry further.

Psana convention is to output detector distance as a negative number, and this is the convention followed by BayFAI. dials.import direcly puts this negative number into the .expt file. 
You can check this distance in the {run_number}-end.data, which is written by BayFAI to the calib/{detectorname}/{somemoredetetctorname}/geometry/ folder. An example file is: 
/sdf/data/lcls/ds/mfx/mfx100904224/calib/Epix10ka2M::CalibV1/MfxEndsta tion.0:Epix10ka2M.0/geometry/5-end.data 
Look at the last line that begins with “IP", in this case the distance would be –106.405 
(converted to mm).

And in the imported.expt file, the corresponding line about detector distance is:

It would be the last number under “origin” under the first entry named “D0” or something similar immediately after “hierarchy”. 
    Weird things we have observed as of 2025/11: 
- The plus/minus sign matters. In dials.image_viewer, a positive number is always enforced. However, it appears that the handedness of coordinate system is preserved. If bayFAI says –106.4, but you manually remove the minus sign in .expt file, the image would flip upside down in the dials.image_viewer. 
- There is some strange offset between .expt value and the value populated in the image viewer. For example, with –106.4 for mfx100904224 run 5, this is populated as 105.6 in the image viewer, but with 106.4 it is populated as 106.8. 
Modify beam X/Y (Center fast/slow) 
If you need to adjust the Center fast/slow entries in the “Unit cell tool” window of the image viewer, you need to save this result somehow by manually editing the .expt file. 
Suppose you need to adjust 50.0 and 40.0 for Center fast/slow.  
Next you need to find the “pixel_size” in the .expt file. Do not look at the values near where you find the detector distance, as values would be 0 – instead, look for pixel_size near the top of the .expt file. In this case, it is [0.1, 0.1]. Then, multiply the values: this means that you would put down 5.0 and 4.0 instead of 50.0 and 40.0.  
    The plus/minus sign, as mentioned above in the detector distance section, can be tricky. In the image viewer, you would find positive as going right and down, but because of the discrepancy between psana and cctbx coordinate system (as of 2025/11), positive in the .expt file means going left and down.

Putting together, this means that you would modify the “origin” in the screenshotted part of the .expt file from [0.0, 0.0, -106.405...] to [-5, 4, -106.405,...].

Refine the geometry with DIALS 
Once you can successfully index some images,  you can refine the geometry further using the indexed reflections. If needed, you can also refine the geometry again after running the ensemble refinement task (just update the file paths to point to ensemble refinement outputs rather than indexing outputs).

Use the first run in the run group we care about (e.g. run 21 for run group 58 trial 9 in this case). 
0. Book-keeping: 
go to the geom folder -- make one right under the experiment tag folder (e.g. common) if you haven’t, e.g. /sdf/data/lcls/ds/mfx/mfx100904224/results/common/geom. Then, make a refine folder for the run group (e.g. refine_rg058) and go into this folder. 
1. combine the indexing output files: 
dials.combine_experiments /path/to/expt /path/to/refl [optional arguments] 
For example, in the geom folder: 
dials.combine_experiments ../../results/r0021/009_rg058/out/*refined*.
expt ../../results/r0021/009_rg058/out/*indexed*.refl reference_from_experiment.detector=0 output.n_subset=1000 
output.n_subset_method=n_refl 
2. Filter reflections: 
cctbx.xfel.filter_experiments_by_rmsd combined.* 
3. Make a 0-level refinement phil file: 
or copy a previous one over: 
cp 
/sdf/data/lcls/ds/mfx/mfx100903824/results/common/geom/refine_rg011/re fine_level0.phil ./ 
Example 0-level refinement phil file looks like this: 
output.experiments=refined_level0.expt output.reflections=refined_level0.refl refinement {

parameterisation {  
    auto_reduction {  
      min_nref_per_parameter = 3  
      action = fail fix *remove  
    } 
    beam {  
      fix = *all in_spindle_plane out_spindle_plane wavelength  
    }  
  }  
  refinery {  
      engine = SimpleLBFGS LBFGScurvs GaussNewton LevMar *SparseLevMar  
  }  
  reflections {  
    outlier { 
      algorithm = null auto *mcd tukey sauter_poon separate_experiments = False separate_panels = True  
    }  
  }  
}

You might want to explore the outlier algorithms. 
4. Perform 0-level refinement on the filtered reflections: 
dials.refine filtered.* refine_level0.phil 
5. Visualize the results and log the terminal output: 
cctbx.xfel.detector_residuals refined_level0.* hierarchy=0 tag=refined 
Example figures output:

Generally, we care more about the bottom row of figures, with the following rule of thumb: 
- The greener plots the better 
- The lower left three figures should have spots cover the detector well to the edge 
- The “refined ΔΨ” figure should have spot concentrated into a small circular region in each panel center

Example terminal output: 
RMSD (microns) 150.5531824354221 
Histogram mode (microns): 132.32253458087138 
Overall mean (microns): 133.50295828414986 
Overall median (microns): 127.85311020060347 
Rayleigh Mean (microns) 165.84170327562524 
Rayleigh RMSD (microns) 187.13232301185118 
Overall radial RMSD (microns) 125.05808894584378 
Overall transverse RMSD (microns) 83.82401144692689

6. Perform 1-level refinement and check the visual results and RMSD improve.  
Example 1-level refinement phil file: 
output.experiments=refined_level1.expt output.reflections=refined_level1.refl refinement { 
  parameterisation {  
    auto_reduction {  
      min_nref_per_parameter = 3  
      action = fail fix *remove  
    } 
    beam {  
      fix = *all in_spindle_plane out_spindle_plane wavelength  
    }  
    detector { 
      fix_list = Group1Tau1 
      hierarchy_level = 1 
    } 
  }  
  refinery {  
      engine = SimpleLBFGS LBFGScurvs GaussNewton LevMar *SparseLevMar  
  }  
  reflections {  
    outlier { 
      algorithm = null auto *mcd tukey sauter_poon separate_experiments = False separate_panels = True

}  
  }  
}

The command to visualize at level 1 is: 
cctbx.xfel.detector_residuals refined_level1.* hierarchy=1 
tag=refined_h1

<!-- handbook-pdf-figures-begin -->

### Figures (from PDF)

![PDF p.31 fig.1](images/intermediate-geometry-refinement_p31_01.png)

![PDF p.32 fig.2](images/intermediate-geometry-refinement_p32_02.jpg)

![PDF p.32 fig.3](images/intermediate-geometry-refinement_p32_03.png)

![PDF p.33 fig.4](images/intermediate-geometry-refinement_p33_04.jpg)

![PDF p.34 fig.5](images/intermediate-geometry-refinement_p34_05.jpg)

![PDF p.35 fig.6](images/intermediate-geometry-refinement_p35_06.png)

![PDF p.37 fig.7](images/intermediate-geometry-refinement_p37_07.jpg)

<!-- handbook-pdf-figures-end -->

