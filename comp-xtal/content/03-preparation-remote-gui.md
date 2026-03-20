---
id: preparation-remote-gui
title: Preparation: Remote access to GUI
---

A note on copy paste between local computer to remote session: the short cut keys can be different so if you fail to paste something keep this in mind. For OnDemand, I couldn’t copy/paste between local (mac) and the VNC session at all... 
S3DF: OnDemand (least lagging, but no copy/paste) 
S3DF OnDemand can be accessed through the following link: 
https://s3df.slac.stanford.edu/ondemand  
From here, navigate to ‘Interactive Apps’ in the top menu and select ‘S3DF’:

Once started, you might want to adjust the image quality:

Then select ‘Launch S3DF’. 
NERSC: ThinLinc 
Follow the official documentation from NERSC on ThinLinc usage: 
https://docs.nersc.gov/connect/thinlinc/ 
It is fairly clear and straightforward (at least on mac). 
S3DF Alternative 1: FastX v4 (StarNet)

After saving the connection, double click

Put in your login credentials, you should see the usual pop up message from S3DF.  
Then, click on the “+” icon on the upper left to start a new session. 
Choose Terminal rather than Desktop (might be historical reason : at some point this prevented a very ugly display issue of the GUI).

Once in the terminal, ssh into psana. 
S3DF Alternative 2: NoMachine 
Click “Add” to create the connection 
Once saved, double click the icon for S3DF, and then double click “Create a new virtual desktop”

Then click the terminal in the desktop, once in the terminal, ssh into psana. 
Other alternatives could be Xming , but might be very slow.

2. Login to the remote session via ssh 
In general, to enable graphics forwarding, you want to put the -Y flag when ssh, e.g.: 
ssh -Y <username>@s3dflogin.slac.stanford.edu 
For S3DF, depending on your ssh config, you might need to have additional ssh into psana: 
ssh –Y psana

3. Source cctbx 
On S3DF 
For psana2:  
source /sdf/group/lcls/ds/tools/cctbx/psana2_setup.sh 
For psana1: 
source /sdf/group/lcls/ds/tools/cctbx/psana1_setup.sh

Tips:

- Do not recommend putting source command in .bashrc (too aggressive with 
Python).  
- A good practice is to keep environment clean, not even base conda environment via .bashrc. 
The setup.sh is a wrapper script of conda_setpaths.sh that comes with the cctbx build but also defines necessary environment variables. 
     The environment variables are different on S3DF vs NERSC.  
If setup.sh is not available, make one as follows: 
S3DF: 
export SIT_DATA=/sdf/group/lcls/ds/ana/data export SIT_PSDM=/sdf/data/lcls/ds/ 
export SIT_ROOT=/sdf/data/lcls/ds export SLURM_PRIORITY_RESERVATION=lcls.onshift umask 002 
source /sdf/group/lcls/ds/tools/cctbx/build/conda_setpaths.sh

On NERSC 
source /global/common/software/cctbx/alcc-recipes/cctbx/activate.sh

<!-- handbook-pdf-figures-begin -->

### Figures (from PDF)

![PDF p.3 fig.1](images/preparation-remote-gui_p03_01.png)

![PDF p.4 fig.2](images/preparation-remote-gui_p04_02.png)

![PDF p.4 fig.3](images/preparation-remote-gui_p04_03.jpg)

![PDF p.5 fig.4](images/preparation-remote-gui_p05_04.png)

![PDF p.5 fig.5](images/preparation-remote-gui_p05_05.png)

![PDF p.5 fig.6](images/preparation-remote-gui_p05_06.png)

![PDF p.6 fig.7](images/preparation-remote-gui_p06_07.png)

<!-- handbook-pdf-figures-end -->

