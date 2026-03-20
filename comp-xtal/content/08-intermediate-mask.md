---
id: intermediate-mask
title: Intermediate: How to make a mask
---

This chapter assumes you have basic familiarity with dials.image_viewer and you know how to average a run. Refer to the previous chapter “Geometry Refinement” if you are not familiar with them. 
Visualize a mask 
Given a pre-made mask (pixels.mask), you can visualize it on an image (std.cbf): 
dials.image_viewer std.cbf load_models=False mask=pixels.mask show_mask=True 
If you didn’t specify show_mask=True, remember to check the box for “Show mask” in the 
“settings” panel that pops up, and the masked pixels will be displayed as red. 
Make a mask 
Steps 0-4 describe how to make masks. After averaging a run, go to the output folder in the terminal. In the following example, the folder is 
/sdf/data/lcls/ds/mfx/mfx101211025/results/doris/results/averages/r001
6/000/out, a case that requires extensive masking. 
0. Dead pixels 
If pixels have 0 standard deviation, they are probably dead pixels. To make a mask of them, use the following script from Fred: 
(base) [mai12345@sdfiana023 000]$ libtbx.python 
Python 3.12.11 | packaged by conda-forge | (main, Jun  4 2025, 14:45:31) [GCC 13.3.0] on linux 
Type "help", "copyright", "credits" or "license" for more information. 
>>> import dxtbx 
>>> img = dxtbx.load("out/std.cbf") might be “max.cbf” 
>>> mask = [m > 0 for m in img.get_raw_data()] 
>>> from libtbx import easy_pickle 
>>> easy_pickle.dump("r0016_stddev.mask", tuple(mask)) 
>>> exit()

Modify the file name or paths in the script as needed. If you are resuming from previous processing, make sure you have sourced the cctbx environment to get libtbx.python. 
Dead pixels can be quite scattered like salt and pepper noise patterns.

1. Panel borders 
Load the image with the dead pixel mask from the previous step as a starting point. 
Click the “Mask tool” under the “Actions” button. To mask panel border, you can increase the value for the “border”.

2. Beam center with a circle and mask by resolution range 
Open the Mask tool as shown in the previous step. 
From my own exploration, it doesn’t look like the Mask tool in dials.image_viewer GUI 
supports cross-panel geometry shape definition.  
If the actual beam center is close to the what dials have (shown by the blue cross, default to image center I believe), you can hack by using resolution range masking. For example, make d_max 200.0:

However, as you can see in this case, the beam center is actually quite shifted. If you want to define an arbitrary circle, you will see that you have to define the circle center within a particular panel, and only the circle on that panel is masked:

In this case, I typed panel 17 and defined the circle (x,y,r) as 1026,30,90. I eyeballed the radius as 90 and got the panel and the position values by hovering my mouse over the

center, and at the bottom of the image you will see some text like “... Readout 17: 
fast=1026 / slow = 30 ...”. 
3. Whole panel due to shadow 
The easiest way to mask whole panels is actually using a command line tool. In this case, suppose I want to mask out the bottom panels which are panel 0-3 (judging from the 
“Readout” number as shown above). In the terminal: 
dials.generate_mask out/std.cbf untrusted.panel=0 untrusted.panel=1 
untrusted.panel=2 untrusted.panel=3 output.mask=panel.mask 
Visually verify if this mask looks good:

If the mask is good, combine this mask with your mask from other step (such as dead pixels) using the same tool: 
dials.generate_mask r0016_stddev.mask panel.mask output.mask=combined.mask 
4. Irregular shape 
The easiest way to make a polygon mask is by clicking where the vertices would be on an image. First open the Mask tool as shown step 1.

Click the Polygon button, and then if you click anywhere on the image, wherever you click would be the vertices. The order matters. Your trace / the edges of the polygon is shown as the cyan clines:

Once you roughly close the shape, click the Polygon button again, and that should properly close the polygon shape for you and mask the region:

5. Good practice notes 
After you think you have made a decent mask by combining some of the steps above, you can save the final mask by clicking “Save mask”.  
Below that button, you can also save the phil parameters of the masking you did through the image_viewer Mask tool, such as making a polygon mask. I strongly recommend you save this every time (change the file name to avoid overwriting) before you close the image_viewer (which you might need to open and close multiple times during a real processing). This is a quantitative way of recording you manual masking and helps reproduce.

<!-- handbook-pdf-figures-begin -->

### Figures (from PDF)

![PDF p.41 fig.1](images/intermediate-mask_p41_01.jpg)

![PDF p.42 fig.2](images/intermediate-mask_p42_02.jpg)

![PDF p.43 fig.3](images/intermediate-mask_p43_03.jpg)

![PDF p.43 fig.4](images/intermediate-mask_p43_04.jpg)

![PDF p.44 fig.5](images/intermediate-mask_p44_05.jpg)

![PDF p.45 fig.6](images/intermediate-mask_p45_06.jpg)

![PDF p.45 fig.7](images/intermediate-mask_p45_07.jpg)

<!-- handbook-pdf-figures-end -->

