---
id: basic-initial-gui
title: Basic: Initial GUI configuration for an experiment
---

0. Source the right cctbx environment 
See Preparation step 3 (‘Source cctbx’) 
1. Configure experiment settings 
The overall configuration of the GUI for an experiment is specified in 
 /sdf/home/<username>/.cctbx.xfel/settings.phil 
Content in this file will pre-populate some entries in the GUI, and conversely, if you fill in or edit the corresponding textboxes in the GUI, it will edit the settings.phil file.  
    If you have never run cctbx.xfel GUI before, you won’t have this folder or this file.

If you are switching between experiments, remember that GUI will overwrite 
~/.cctbx.xfel/settings.phil, so it is good practice to always save a copy of the existing settings.phil before running. 
Usually you would copy a previous settings.phil file as a template to start with (and make the .cctbx.xfel folder if it doesn’t exist yet): 
cp /sdf/home/<username>/.cctbx.xfel/settings.phil <experiment_file> 
e.g. for Summers: /sdf/home/m/mai12345/.cctbx.xfel/mfx100904224.phil 
The content of this file looks like this:

It is ok to start the GUI from scratch or from a partially filled settings.phil file. But if you did put down the “output_folder”, Make sure paths already exist, as the GUI will not create new folders and instead just crashes or freezes  with terminal output errors. 
2. Start GUI 
Run: cctbx.xfel in terminal. Launching cctbx can take a minute. 
When you launch the GUI using this PHIL phil, you will see the following window and you can spot some of the corresponding entries such as “Experiment Tag” (experiment_tag), “Output” (output_folder), “Facility”(facility.name), and “Experiment” 
(facility.lcls.experiment) from the setting.phil file.

Fill fields if not already populated by the experiment settings.phil file:

The output field in the text box above is: 
 /sdf/data/lcls/ds/mfx/mfx100904224/results/kmdalton/results

Experiment Tag and Output Folder 
Conventionally, the experiment tag and your process folder (relative path to the experiment folder) should match, but it looks like this is not strictly enforced. In this example, we have an experiment tag as “common”, but the processing folder (relative path) can be “pam” (used in the examples below) or “kmdalton” (in the screenshot above). 
Unless you are the official processing person (in which case the output folder should be 
“common” (relative path)), you are recommended to make a folder for yourself (e.g. named 
“pam”). 
The overall experiment folder is:

And the GUI expects your processing folder (absolute path) would be the following:

DB Credentials 
Modify DB credentials as needed, this corresponds to the “db” section in the settings.phil file. Name and user are usually the experiment.

Password: lcls

The buttons at the bottom of the DB window sometimes disappear (for example, when running cctbx.xfel via OnDemand). You can exit out of the window by using the return or escape key on your keyboard.

Options: 
Leave them unselected.

Advanced Settings 
Modify advanced settings as needed -- this corresponds to the “mp” section of the settings.phil file.  
    Make sure that the “Environment setup script” matches with the script you used in step 
0 to source cctbx.

Most of the other entries are related to slurm job configuration, including the “Extra submission arguments” (which corresponds to “extra_options” under “mp” as a string). 
Milano has 128 cores and WEKA takes 8 cores, use no more than 120 here as number of processors per node. 
The slurm account in Extra submission arguments” should match the experiment you are processing.

If real-time processing during beamtime, you can add “--reservation=lcls:onshift”, but use it wisely: the job priority is higher but you are restricted to 10 nodes.

3. Populating runs  
In GUI, click Watch for new runs (Hold until button turns yellow.) The buttons can be a bit laggy. 
    At most one person (instance of GUI) can watch at any time, so it is good practice to turn the watch off when not needed. For reprocessing, you only need to turn it on for a few seconds to load all the run information once.

You should see runs populated under the “Run” page. 
4. Tagging runs 
To add a tag, click “Manage Tags” at the bottom.  
To associate an added tag for multiple runs, click “Change Tags on Multiple Runs” at the bottom. 
For real-time processing, it is helpful to automatically tag an incoming run if you know the sample condition won’t change for a while. In this case, click “Manage Persistant Tags” at the bottom. 
    if GUI crashes during real-time processing, when you relaunch the GUI, you need to configure this persistent tagging again. Otherwise before you know there will be many untagged runs coming in.

<!-- handbook-pdf-figures-begin -->

### Figures (from PDF)

![PDF p.8 fig.1](images/basic-initial-gui_p08_01.png)

![PDF p.9 fig.2](images/basic-initial-gui_p09_02.jpg)

![PDF p.10 fig.3](images/basic-initial-gui_p10_03.jpg)

![PDF p.11 fig.4](images/basic-initial-gui_p11_04.png)

![PDF p.11 fig.5](images/basic-initial-gui_p11_05.jpg)

![PDF p.12 fig.6](images/basic-initial-gui_p12_06.png)

![PDF p.13 fig.7](images/basic-initial-gui_p13_07.jpg)

<!-- handbook-pdf-figures-end -->

