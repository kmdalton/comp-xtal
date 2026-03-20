---
id: preparation-remote-gui
title: Preparation: Remote access to GUI
---

A note on copy/paste between your local computer and the remote session: shortcut keys can differ, so if paste fails, keep that in mind. For OnDemand, copy/paste between local (Mac) and the VNC session did not work at all.

### S3DF: OnDemand (least lagging, but no copy/paste)

S3DF OnDemand: <https://s3df.slac.stanford.edu/ondemand>

From there, open **Interactive Apps** in the top menu and choose **S3DF**. After it starts, you may want to lower image quality for responsiveness, then choose **Launch S3DF**.

### NERSC: ThinLinc

Follow NERSC’s ThinLinc documentation: <https://docs.nersc.gov/connect/thinlinc/> — it is fairly clear and straightforward (at least on Mac).

### S3DF alternative 1: FastX v4 (StarNet)

After saving the connection, double-click it. Enter your login credentials; you should see the usual S3DF prompt. Click the **+** icon at the upper left to start a new session. Choose **Terminal** rather than Desktop (this historically avoided a bad display issue with the GUI). In the terminal, `ssh` into **psana**.

### S3DF alternative 2: NoMachine

Click **Add** to create the connection. After saving, double-click the S3DF icon, then **Create a new virtual desktop**. Open a terminal in the desktop, then `ssh` into **psana**.

Other options (e.g. Xming) exist but can be very slow.

### Login to the remote session via SSH

To enable graphics forwarding, use `-Y` when you `ssh`, for example:

```bash
ssh -Y <username>@s3dflogin.slac.stanford.edu
```

Depending on your SSH config, you may need an extra hop into psana:

```bash
ssh -Y psana
```

### Source cctbx

**On S3DF**

- **psana2:** `source /sdf/group/lcls/ds/tools/cctbx/psana2_setup.sh`
- **psana1:** `source /sdf/group/lcls/ds/tools/cctbx/psana1_setup.sh`

**Tips**

- Avoid putting `source` in `.bashrc` (too aggressive for Python).
- Prefer a clean environment; even avoiding activating base Conda via `.bashrc` is good practice.
- `setup.sh` is a wrapper around `conda_setpaths.sh` from the cctbx build and sets required environment variables (they differ on S3DF vs NERSC).

If `setup.sh` is missing, create one. **S3DF example:**

```bash
export SIT_DATA=/sdf/group/lcls/ds/ana/data
export SIT_PSDM=/sdf/data/lcls/ds/
export SIT_ROOT=/sdf/data/lcls/ds
export SLURM_PRIORITY_RESERVATION=lcls.onshift
umask 002
source /sdf/group/lcls/ds/tools/cctbx/build/conda_setpaths.sh
```

**On NERSC**

```bash
source /global/common/software/cctbx/alcc-recipes/cctbx/activate.sh
```

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
