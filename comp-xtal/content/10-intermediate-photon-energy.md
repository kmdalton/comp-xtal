---
id: intermediate-photon-energy
title: Intermediate: Photon energy calibration
---

Correct energy can help indexing. To perform energy calibration, go to the “Energy” page of the GUI. 
0. Populate the table 
On the upper left panel, click “Add Row”, then click on each entry under “Run” and “Notch 
Energy” to manually fill a value. (You need to click “Add Row” for each new row to add.)

Only support one energy per run rather than a scan where many energies within a run. 
1. Run Calibration 
Once done, click “Run Calibration.” At the bottom, the sentinel for “Calib Worker” should turn yellow indicating work in progress. This would take a few seconds, and once done, the sentinel becomes green, and you should see something like this:

Select the same runs for Ebeam Calibration (lower left panel) and click “Run Calibration.” 
This can take a few minutes. Once it’s done, you should see another plot “Ebeam vs 
Calibrated FEE” populated and the value for “Ebeam offset” value should also be there under “Calibration results”:

If for some reason the job failed and the sentinel is red, clicking anything on this page might not get a response. After you make you corrections, you can try switch to a different page like “Trials” and then switch back to “Energy” to properly refresh the sentinel.  
    I am having trouble with other experiments for the “Ebeam Calibration.” For mfx100903824 (psana1), run 4-8 throws error on the terminal that these runs are not in any run group. For run 14, 16, and 18, I see the following error on the terminal: 'Unknown 
DetInfo device type: feespec (source: feespec)’. Unclear why and how to solve it. 
    I am having trouble with other experiments for the “Energy Calibration.” For mfx101262725 (psana2), run 225-234, I get the following error on the terminal: 
unsupported operand type(s) for /=: 'NoneType' and 'int'. Unclear why and how to solve it. 
2. Use the results for run group definition 
The calibration results are shown at the lower right panel, which you can save to a file if you click the button, and the file looks like this:  
(base) [mai12345@sdfiana026 phils]$ cat fee_calib.phil spectrum_eV_per_pixel=0.0689

spectrum_eV_offset=9451.2432 
ebeam_eV_offset=-10.35

Enter the two spectrum_eV related values when defining the run group (scroll down to see the corresponding entries in the GUI).

Alternative method 
In case something goes wrong with the GUI, the corresponding command line tool for FEE 
calibration is xfel.fee_calib <expname> <run>:<notch_energy>. For example: 
[mai12345@sdfiana003 ~]$ xfel.fee_calibration experiment=mfx101259025 
38:9540 39:9542 40:9544 41:9546 
Processing run 38... 
Found 1000 events with FEE, 0 events without (1000 total) 
Processing run 39... 
Found 2000 events with FEE, 0 events without (2000 total) 
Processing run 40... 
Found 3000 events with FEE, 0 events without (3000 total) 
Processing run 41... 
Found 4000 events with FEE, 0 events without (4000 total)

Calibrated eV offset of 9452.329454096232 and eV per pixel of 
0.06813544632577721 
wrote calibrated values to fee_calib.out 
[mai12345@sdfiana003 ~]$ cat fee_calib.out using experiment=mfx101259025 38:9540 39:9542 40:9544 41:9546, eV_offset=9452.329454096232 eV_per_pixel=0.06813544632577721

The command should also pop out familiar figures like this:

<!-- handbook-pdf-figures-begin -->

### Figures (from PDF)

![PDF p.50 fig.1](images/intermediate-photon-energy_p50_01.png)

![PDF p.51 fig.2](images/intermediate-photon-energy_p51_02.png)

![PDF p.52 fig.3](images/intermediate-photon-energy_p52_03.png)

![PDF p.53 fig.4](images/intermediate-photon-energy_p53_04.png)

![PDF p.54 fig.5](images/intermediate-photon-energy_p54_05.png)

<!-- handbook-pdf-figures-end -->

