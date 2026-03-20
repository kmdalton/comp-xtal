---
id: basic-initial-gui
title: Basic: Initial GUI configuration for an experiment
---

### 0. Source the right cctbx environment

See **Preparation** → **Source cctbx** (SSH section above).

### 1. Configure experiment settings

The overall GUI configuration for an experiment lives in:

`/sdf/home/<username>/.cctbx.xfel/settings.phil`

That file pre-populates GUI fields, and edits in the GUI write back to `settings.phil`. If you have never run the cctbx.xfel GUI before, you may not have this folder or file yet.

If you switch experiments, the GUI can overwrite `~/.cctbx.xfel/settings.phil`, so save a copy before running. You can copy an existing file as a template (create `.cctbx.xfel` if needed):

```bash
cp /sdf/home/<username>/.cctbx.xfel/settings.phil <experiment_file>
```

Example (Summers): `/sdf/home/m/mai12345/.cctbx.xfel/mfx100904224.phil`

The file content structure matches what the GUI shows (screenshots in **Figures** below).

You may start from scratch or from a partial `settings.phil`. If you set **output_folder**, those paths must already exist—the GUI will not create them and may crash or freeze.

### 2. Start GUI

Run **`cctbx.xfel`** in a terminal (startup can take about a minute). With your PHIL loaded, you should see entries such as **Experiment Tag** (`experiment_tag`), **Output** (`output_folder`), **Facility** (`facility.name`), and **Experiment** (`facility.lcls.experiment`).

Fill any fields not already set from `settings.phil`.

Example output path shown in the GUI:

`/sdf/data/lcls/ds/mfx/mfx100904224/results/kmdalton/results`

**Experiment tag and output folder**

Conventionally the experiment tag and process folder (relative to the experiment folder) should match, but this is not always enforced. For example the tag may be **common** while the processing folder (relative path) is **pam** or **kmdalton** (as in the screenshots).

Unless you are the official processing person (in which case the output folder is usually **common**), create a folder for yourself (e.g. **pam**). The overall experiment folder is set by the facility layout; the GUI expects your processing folder as an **absolute path**.

**DB credentials**

Match the **db** section in `settings.phil`. Name and user are usually the experiment. Password is often **lcls**.

If bottom buttons in the DB window disappear (e.g. via OnDemand), exit with **Return** or **Escape**.

**Options**

Leave them unselected unless you know you need them.

**Advanced settings**

Correspond to the **mp** section in `settings.phil`. The **Environment setup script** must match how you sourced cctbx in step 0.

Other fields are mostly Slurm-related, including **Extra submission arguments** (`extra_options` under **mp** as a string). Milano has 128 cores and WEKA uses 8—use at most ~120 processors per node. The Slurm account in extra arguments should match the experiment.

For real-time beamtime work you may add `--reservation=lcls:onshift` (higher priority, limited to 10 nodes—use sparingly).

### 3. Populating runs

In the GUI, click **Watch for new runs** (hold until the button turns yellow). Buttons can lag.

Only one GUI instance should watch at a time—turn watch off when not needed. For reprocessing, a short watch is enough to load run metadata.

Runs should appear under the **Run** page.

### 4. Tagging runs

- **Manage Tags** — add tags.
- **Change Tags on Multiple Runs** — apply tags to many runs.
- **Manage Persistent Tags** — auto-tag incoming runs when the sample is stable (change when the sample changes).

If the GUI crashes during real-time processing, reconfigure persistent tagging after relaunch, or untagged runs can pile up.

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
