---
id: intermediate-realtime-s3df
title: Intermediate: Prepare for real-time usage during beamtime (S3DF)
---

### Before the beamtime

**General**

- Check that the experiment folder has been set up on S3DF and is visible on eLog.
- Collect dark runs (test takepeds/makepeds).
- Collect calibrant data and run BayFAI (during commissioning).

**Note on BayFAI / geometry (2026/02)**

See the LUTE documentation for setting up and running BayFAI to estimate geometry: <https://slac-lcls.github.io/lute/dev/usage/tasks/bayfai/bayfai/>

As of 2026/02, this means following the linked instructions in the experiment folder. After setup, the BayFAI workflow should auto-populate on eLog → **Workflow** → **Definitions**; adjust as needed (e.g. set **Trigger** to **MANUAL** rather than end of run, tune Slurm arguments such as `--ntasks`).

**Database**

- Users must request MariaDB on their form to use the cctbx.xfel GUI. If that is missing, email **pcds-datamgt-I** to set it up.
- If the GUI shows a database error on launch, the DB is not ready yet.

Verify with:

```bash
mysql -h 172.24.5.182 -u <experiment> <experiment> -p
```

See **Debugging tips** for more `mysql` commands.

**GUI readiness**

Run test jobs (e.g. energy calibration) before beamtime:

- Can you launch the GUI (remote access + sourced cctbx)?
- Can the GUI reach MariaDB and show runs under **Watch for new runs**?
- Can you submit simple jobs (e.g. average a run and view the image)?

**Analysis info to have ready**

- Unit cell and space group; reference PDB if available.
- A PHIL template for indexing/trial definition (from users or a recent beamtime).
- Optional: reference geometry `.expt` (if not using BayFAI).
- Optional: reference mask from a recent beamtime.

### During the beamtime

The main question is whether enough data exist to move on. Ideally you reach merged results and inspect stats; in practice, indexed image count is a quick gauge.

**Make initial files for indexing**

- No geometry yet → average a run and create one.
- No mask yet → average a run and build one.

Initial geometry/PHIL are rarely perfect; expect iterations on energy calibration, geometry refinement, mask updates, and spot-finding PHIL—similar to offline reprocessing.

**Hit / indexing progress**

Watch **Run Stats** and **Unit Cell** for indexing rate and counts. Tips:

- Use a **persistent tag** for incoming runs when the sample is stable (change it when the sample changes).
- Set `integrate=False` on the trial for indexing-only; remove it or run ensemble refinement before scaling/merging.

**Merging progress**

Use the **Merging stats** tab. **Active only** refers to the dataset (optional). Leave **Dataset version** as **All** to see stats evolve across versions.

**Do not** pick a single dataset version—plotting can fail (**Merging Stats** sentinel turns red). Switch tabs and return, or relaunch the GUI to recover. Plotting can be slow; watch the sentinel: if it stays idle and does not go yellow (working) or goes red, it may be stuck.

You want metrics to rise and then plateau when data are sufficient. Do not mix different samples in one dataset or trajectories become misleading. This tab is for “do we need more data?”; for full merging statistics, use the `...main.log` file in the merging output folder.

<!-- handbook-pdf-figures-begin -->

### Figures (from PDF)

![PDF p.27 fig.1](images/intermediate-realtime-s3df_p27_01.png)

![PDF p.30 fig.2](images/intermediate-realtime-s3df_p30_02.png)

<!-- handbook-pdf-figures-end -->
