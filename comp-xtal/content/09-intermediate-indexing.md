---
id: intermediate-indexing
title: Intermediate: Indexing result improvement
---

Diagnostics 
“Run Stats” tab of the GUI

You might need to hide Options to see the numbers at the bottom. "%xtal" (behind the %solv) is the hit rate and "%idx" is the indexing rate (also plotted as the blue line in the middle panel). The numbers in the parenthesis are number of images with multiple lattices. 
I would also look at the top panel, where blue dot is indexed and grey dot is not, and ideally there are quite a bit of blue on top without too much grey stuff visible. It is possible to click on the dots to launch the corresponding image via dials.image_viewer to see if indexing and spotfinding works as expected. 
“Unit Cell” tab of the GUI

Ideally we should see nice and narrow Gaussians centered at expected cell parameters. 
Low indexing rate 
Is your spot finding good? Are there clearly visible spots that are strong and lattice-like but not picked up somehow? 
- Do you need to make a better mask? 
- Explore via dials.image_viewer on the parameters for thresholding pixels 
Once confirmed strong spots are found, explore indexing related knobs: 
- Indexing algorithm parameters: consider using indexing.stills.method_list=fft1d fft3d real_space_grid_search to your phil parameter (trial definition or run group extra phil parameter).  
- Geometry: 
o Perform geometry refinement at both level 0 and 1. Could also explore different choices (mcd, tukey, sauter_poon) for reflections.outlier.algorithm o Try proceed to the Ensemble refinement task for updated cell and geometry 
Strange unit cell distribution 
If the unit cell distribution shape is not a nice Gaussian (but skewed or bimodal): 
- Do you need to (further) refine the geometry? 
- Was there energy drift?

- Is there indexing ambiguity for this space group + unit cell?

<!-- handbook-pdf-figures-begin -->

### Figures (from PDF)

![PDF p.47 fig.1](images/intermediate-indexing_p47_01.jpg)

![PDF p.48 fig.2](images/intermediate-indexing_p48_02.png)

<!-- handbook-pdf-figures-end -->

