# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pydivide


#TVarFigure1D

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

# fake data
dates_d = pd.date_range('2017-11-01', '2017-12-31', freq='D')
df = pd.DataFrame(np.random.randint(1, 20, (dates_d.shape[0], 1)))
df.index = dates_d
dates_h = pd.date_range('2017-11-01', '2017-12-31', freq='H')
df_h = pd.DataFrame(np.random.randint(1, 20, (dates_h.shape[0], 1)))
df_h.index = dates_h

# #two graphs
fig, axes = plt.subplots(nrows=1, ncols=1, sharex=True)
axes.xaxis.grid(b=True, which='major', color='black', linestyle='--', alpha=1) #add xaxis gridlines
axes.set_xlim(min(dates_d), max(dates_d))
axes.set_title('Weekend days', fontsize=10)

time_start = ["2017-11-28 04:27:05","2017-12-01 04:27:05"]
time_end = ["2017-11-30 04:27:05","2017-12-05 04:27:05"]

def highlight_datetimes(time_start,time_end,color,ax):
    dates_to_highlight_start = []
    for date in time_start:
        #date format: "2017-11-02 04:27:05"
        date = date.replace('-',' ')
        date = date.replace(':',' ')
        y,mo,d,h,mn,s = date.split(' ')
        dates_to_highlight_start = dates_to_highlight_start + [datetime.datetime(int(y),int(mo),int(d),int(h),int(mn),int(s))]
        
    dates_to_highlight_end = []
    for date in time_end:
        #date format: "2017-11-02 04:27:05"
        date = date.replace('-',' ')
        date = date.replace(':',' ')
        y,mo,d,h,mn,s = date.split(' ')
        dates_to_highlight_end = dates_to_highlight_end + [datetime.datetime(int(y),int(mo),int(d),int(h),int(mn),int(s))]
        
    for i, val in enumerate(dates_to_highlight_start):
        ax.axvspan(dates_to_highlight_start[i], dates_to_highlight_end[i], facecolor=color, edgecolor='none', alpha=.5)




def timebar(time_list,color,width):
    dates_to_highlight = []
    for date in time_start:
        #date = "2017-11-39 04:27:05"
        date = date.replace('-',' ')
        date = date.replace(':',' ')
        y,mo,d,h,mn,s = date.split(' ')
        dates_to_highlight = dates_to_highlight + [datetime.datetime(int(y),int(mo),int(d),int(h),int(mn),int(s))]
        for i, val in enumerate(dates_to_highlight):
            plt.axvline(x=dates_to_highlight[i],color=color,linewidth = width)

#highlight_datetimes(time_start, time_end,'blue', axes)#[0])
timebar(time_start, 'magenta', '7')


plt.show()