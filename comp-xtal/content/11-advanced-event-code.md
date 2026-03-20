---
id: advanced-event-code
title: Advanced: Event code handling
---

Helpful past experiments to look at include mfxl1015222 – Lane and mfx101262725 – 
Follmer (and other T-jump experiments in the past). If there are issues that require addressing CCTBX source code, dxtbx/src/dxtbx/format/FormatXTC.py is a key file to look at. 
Sanity check if event code is set up properly for a run 
Tthe following script list_event_codes.py by Fred is helpful: 
from psana import DataSource from sys import argv

args = argv[1:] exp = str(args[0]) run = int(args[1]) event_codes = [int(arg) for arg in args[2:]]

ds = DataSource(exp=exp, run=run, detectors=['timing'], max_events=100) myrun = next(ds.runs()) timing = myrun.Detector('timing') for nevt,evt in enumerate(myrun.events()): 
    allcodes = timing.raw.eventcodes(evt) evtcodes = [i for i, val in enumerate(allcodes) if val != 0] print(evtcodes)

To use this script, make sure you have activated psana2 environment, and then:  
python list_event_codes.py <exp> <run> 
To understand the output, for example, event code 201-213 (except for 208) was set up for this T-jump experiment, and the first few line of results look like this: 
(ps_20241122) [mai12345@sdfiana002 dorismai]$ python list_event_codes.py mfx101262725 
121 
[0, 1, 9, 10, 40, 41, 42, 84, 88, 99, 101, 119, 122, 123, 128, 132, 135, 137, 140, 141, 142, 151, 152, 153, 155, 157, 158, 165, 201] 
[0, 1, 9, 10, 11, 40, 84, 89, 99, 101, 119, 122, 123, 128, 132, 135, 137, 140, 151, 152, 153, 155, 157, 158, 202] 
[0, 1, 9, 10, 40, 41, 84, 89, 99, 101, 119, 122, 123, 128, 132, 135, 137, 140, 141, 151, 152, 153, 155, 157, 158, 165, 203]

[0, 1, 9, 10, 11, 12, 13, 14, 15, 16, 40, 84, 88, 119, 122, 123, 128, 132, 135, 137, 140, 151, 152, 153, 155, 157, 158, 204] 
[0, 1, 9, 10, 40, 41, 42, 43, 44, 45, 46, 84, 88, 99, 101, 119, 122, 123, 128, 131, 132, 135, 137, 140, 141, 142, 143, 144, 145, 146, 149, 151, 152, 154, 155, 157, 158, 159, 165, 169, 205] 
[0, 1, 9, 10, 11, 40, 84, 88, 99, 101, 119, 122, 123, 128, 132, 135, 137, 140, 151, 152, 153, 155, 157, 158, 206] 
You can see that the last number of each shot (each array) iterates among 201 to 213 as expected. 
Specify event code in cctbx 
You can filter to process data associated with only one event code by providing “Extra XTC 
format parameters” when defining a run group.  
For example, for the T-jump experiment mfx101262725, event code 203 is reserved for the laser ON status. To process data associated laser on, you would put in the following lines: 
filter.evr_address=evr0 
filter.required_present_codes=203 
These lines are added in addition to the other lines you might need, such as 
“mode=psana2_idx” for psana2 data.
