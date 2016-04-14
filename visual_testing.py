#
#
# THIS TESTING MODULE REQUIRES THE USER TO TYPE:
# conda install -c https://conda.binstar.org/mwcraig vpython
# INTO THEIR COMMAND PROMPT
#

    
from visual import *
from visual.controls import *
from PIL import Image
import math
import os
import csv
import wx


#Buttons event handlers
def axes_on(evt):
    geo_x_axis.opacity = 1
    geo_y_axis.opacity = 1
    geo_z_axis.opacity = 1
    x_label.visible = True
    y_label.visible = True
    z_label.visible = True
    
def axes_off(evt):
    geo_x_axis.opacity = 0
    geo_y_axis.opacity = 0
    geo_z_axis.opacity = 0
    x_label.visible = False
    y_label.visible = False
    z_label.visible = False

def vec_on(evt):
    for curve in curve_list:
        curve.visible = True
 
def vec_off(evt):
    for curve in curve_list:
        curve.visible = False
    
def setTime(evt):
    value = s1.GetValue()
    maven.pos = (spacecraft_x[value], spacecraft_y[value], spacecraft_z[value])
    sun_val = float(value)/(len(spacecraft_x)-1)
    sun.direction = (math.cos(sun_val*2*math.pi), math.sin(sun_val*2*math.pi), 0)


#Read in Spacecraft and MAG data from 2015-04-15
spacecraft_x = []
spacecraft_y = []
spacecraft_z = []
mag_x = []
mag_y = []
mag_z = []
with open('C:/Anaconda/Hello2.txt', 'rb') as csvfile:
    spamreader=csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        asdf = row[0][1:]
        spacecraft_x.append(float(asdf)/3397.0)
        spacecraft_y.append(float(row[1])/3397.0)
        spacecraft_z.append(float(row[2])/3397.0)
        mag_x.append(float(row[3])/124.0)
        mag_y.append(float(row[4])/124.0)
        mag_z.append(float(row[5])/124.0)

#Get the Mars Texture
full_path=os.path.realpath(__file__)
path, filename = os.path.split(full_path)
name = "mars_2k_color"
width=2048
height=1024
im = Image.open(path+'/basemaps/'+name+".jpg")
mars_tex = materials.texture(data=im, mapping='spherical')


#Set up the Window
w = window(menus=True, title="MAVEN",
           x=0, y=0, width=1000, height=700)
d = display(window=w, x=10, y=10, width=600, height=600)

#Set up the buttons
p = w.panel
axes_disp_on = wx.Button(p, label='Display Axes', pos=(650,10))
axes_disp_on.Bind(wx.EVT_BUTTON, axes_on)
axes_disp_off = wx.Button(p, label='Remove Axes', pos=(750,10))
axes_disp_off.Bind(wx.EVT_BUTTON, axes_off)

vec_disp_on = wx.Button(p, label='Display Mag', pos=(650,50))
vec_disp_on.Bind(wx.EVT_BUTTON, vec_on)
vec_disp_off = wx.Button(p, label='Remove Mag', pos=(750,50))
vec_disp_off.Bind(wx.EVT_BUTTON, vec_off)

#Set up the slider bar
s1 = wx.Slider(p, pos=(650,105), size=(200,20), minValue=0, maxValue=len(spacecraft_x)-1)
s1.Bind(wx.EVT_SCROLL, setTime)
wx.StaticText(p,label="Time Slider Bar", pos=(650,90))


#Put the objects into the scene
mars = sphere(pos=(0,0,0), radius=1, material=mars_tex, index=0)
mars.rotate(angle=pi/2, axis=(1,0,0))
mars.rotate(angle=-pi/2, axis=(0,0,1))
maven = sphere(pos=(spacecraft_x[0], spacecraft_y[0], spacecraft_z[0]), radius=.1, color=color.red)
geo_x_axis = arrow(pos=vector(0,0,0), axis=vector(3,0,0), color=color.white, shaftwidth=0.03, headwidth=.06, opacity = 0)
geo_y_axis = arrow(pos=vector(0,0,0), axis=vector(0,3,0), color=color.white, shaftwidth=0.03, headwidth=.06, opacity = 0)
geo_z_axis = arrow(pos=vector(0,0,0), axis=vector(0,0,3), color=color.white, shaftwidth=0.03, headwidth=.06, opacity = 0)
sun = distant_light(direction=(1,0,0), color=color.white)
spacecraft_position=curve(x=spacecraft_x, y=spacecraft_y, z=spacecraft_z)
x_label = label(pos=(3.1,0,0), text='x', visible=False)
y_label = label(pos=(0,3.1,0), text='y', visible=False)
z_label = label(pos=(0,0,3.1), text='z', visible=False)

curve_list=[]
for i in range(1, len(mag_x)-1):
    curve_list.append(curve(x=[spacecraft_x[i], spacecraft_x[i]+mag_x[i]], y=[spacecraft_y[i], spacecraft_y[i]+mag_y[i]],z=[spacecraft_z[i], spacecraft_z[i]+mag_z[i]], visible=False))

#Every program needs to end with an infinite loop for some reason (that's what it says to do)
while True:
    rate(30)

