# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pydivide

import matplotlib.pyplot as plt
import datetime
import random

x = [datetime.datetime.now() + datetime.timedelta(hours=i) for i in range(12)]
print(x)
y = [i+random.gauss(0,1) for i,_ in enumerate(x)]
# plot
plt.plot(x,y)
# beautify the x-labels
plt.gcf().autofmt_xdate()
plt.show()


# def timebar(time,thick=2,color='red',opacity=0.5,rng='no'):
#     if rng == 'yes' or rng=='y':
#         tleft = min(time)
#         tright = max(time)
#         plt.axvspan(tleft, tright, color=color, alpha=opacity)
#     else:
#         if len(time) > 1:
#             for t in time:
#                 axes = plt.gca()
#                 xl = axes.get_xlim()
#                 xrng = xl[1]-xl[0]
#                 xthick = xrng*thick/100
#                 tleft = t - xthick
#                 tright = t + xthick
#                 plt.axvspan(tleft, tright, color=color, alpha=opacity)
#         else:
#             axes = plt.gca()
#             #xl = axes.get_xlim()
#             #xrng = xl[1]-xl[0]
#             #xthick = xrng*thick/100
#             #tleft = time - xthick
#             #tright = time + xthick
#             #plt.axvspan(tleft, tright, color=color, alpha=opacity)
#             fig = plt.gcf()
#             size = fig.get_size_inches()*fig.dpi
# 
# timebar('03-28-19',thick=2,color = 'teal',opacity = 0.2,rng='no')
# plt.show()

def timebar(starttime,endtime,color='red',opacity=0.5):
    
        plt.axvspan(starttime, endtime, color=color, alpha=opacity)

timebar('03-28-19','03-29-19',color = 'teal',opacity = 0.2)
plt.show()