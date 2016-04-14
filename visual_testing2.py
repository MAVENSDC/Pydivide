#
#
# THIS TESTING MODULE REQUIRES THE USER TO TYPE:
# conda install -c https://conda.binstar.org/mwcraig vpython
# INTO THEIR COMMAND PROMPT
#

    
from visual import *
from visual.controls import *
from visual.graph import *
from PIL import Image
import math
import os
import csv
import wx


#Buttons event handlers
def axes_display(evt):
   if axes_disp.GetValue():
       geo_x_axis.opacity = 1
       geo_y_axis.opacity = 1
       geo_z_axis.opacity = 1
       x_label.visible = True
       y_label.visible = True
       z_label.visible = True
   else:
        geo_x_axis.opacity = 0
        geo_y_axis.opacity = 0
        geo_z_axis.opacity = 0
        x_label.visible = False
        y_label.visible = False
        z_label.visible = False

def sun_axis_display(evt):
    if sun_axis_disp.GetValue():
        sun_axis.opacity = 1
    else:
        sun_axis.opacity = 0

def mag_vector_display(evt):
    if mag_disp.GetValue():
        for curve in curve_list:
            curve.visible = True
    else:
        for curve in curve_list:
            curve.visible = False

    
def setTime(evt):
    value = s1.GetValue()
    maven.pos = (spacecraft_x[value], spacecraft_y[value], spacecraft_z[value])
    sun.direction = (math.cos(solar_lon[value]*math.pi/180), math.sin(solar_lon[value]*math.pi/180), math.sin(solar_lat[value]*math.pi/180))
    sun_axis.axis = vector(3*math.cos(solar_lon[value]*math.pi/180), 3*math.sin(solar_lon[value]*math.pi/180), 3*math.sin(solar_lat[value]*math.pi/180))
    
def toggleMaps(evt):
    choice=t1.GetSelection()
    if choice==0:
        mars.material = mars_tex
    if choice==1:
        mars.material = mola_tex
    if choice==2:
        mars.material = mag_tex


#Read in Spacecraft and MAG data from 2015-04-15
spacecraft_x = []
spacecraft_y = []
spacecraft_z = []
mag_x = []
mag_y = []
mag_z = []
solar_lon = []
solar_lat = []
hplus_temp = []
with open('C:/Anaconda/Hello3.txt', 'rb') as csvfile:
    spamreader=csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        asdf = row[0][1:]
        spacecraft_x.append(float(asdf)/3397.0)
        spacecraft_y.append(float(row[1])/3397.0)
        spacecraft_z.append(float(row[2])/3397.0)
        mag_x.append(float(row[3])/124.0)
        mag_y.append(float(row[4])/124.0)
        mag_z.append(float(row[5])/124.0)
        solar_lon.append(float(row[6]))
        solar_lat.append(float(row[7]))
        hplus_temp.append(float(row[8]))

#Get the Mars Texture
full_path=os.path.realpath(__file__)
path, filename = os.path.split(full_path)
width=2048
height=1024

name = "mars_2k_color"
im = Image.open(path+'/basemaps/'+name+".jpg")
im = im.resize((width,height), Image.ANTIALIAS)
mars_tex = materials.texture(data=im, mapping='spherical')

name = "MOLA_color_2500x1250"
im = Image.open(path+'/basemaps/'+name+".jpg")
im = im.resize((width,height), Image.ANTIALIAS)
mola_tex = materials.texture(data=im, mapping='spherical')

name = "MAG_Connerny_2005"
im = Image.open(path+'/basemaps/'+name+".jpg")
im = im.resize((width,height), Image.ANTIALIAS)
mag_tex = materials.texture(data=im, mapping='spherical')


#Set up the Window
w = window(menus=True, title="MAVEN",
           x=0, y=0, width=1000, height=700)
d = display(window=w, x=10, y=10, width=600, height=600)

#Set up the buttons
p = w.panel

wx.StaticText(p,label="Label Options", pos=(650,10))
axes_disp = wx.ToggleButton(p, label='Display Axes', pos=(650, 35))
axes_disp.Bind(wx.EVT_TOGGLEBUTTON, axes_display)
sun_axis_disp = wx.ToggleButton(p, label='Sun Vector', pos=(650, 75))
sun_axis_disp.Bind(wx.EVT_TOGGLEBUTTON, sun_axis_display)
wx.StaticText(p,label="Data Options", pos=(650,125))
mag_disp = wx.ToggleButton(p, label='Display Mag', pos=(650, 150))
mag_disp.Bind(wx.EVT_TOGGLEBUTTON, mag_vector_display)


#Set up Radio Buttons
t1 = wx.RadioBox(p, pos=(800, 20), choices = ['MDIM', 'MOLA', 'MAG'], style=wx.RA_SPECIFY_ROWS)
t1.Bind(wx.EVT_RADIOBOX, toggleMaps)

#Set up the slider bar
s1 = wx.Slider(p, pos=(650,265), size=(200,20), minValue=0, maxValue=len(spacecraft_x)-1)
s1.Bind(wx.EVT_SCROLL, setTime)
wx.StaticText(p,label="Time Slider Bar", pos=(650,250))



#Put the objects into the scene
mars = sphere(pos=(0,0,0), radius=1, material=mars_tex, index=0)
mars.rotate(angle=pi/2, axis=(1,0,0))
mars.rotate(angle=-pi/2, axis=(0,0,1))
maven = sphere(pos=(spacecraft_x[0], spacecraft_y[0], spacecraft_z[0]), radius=.1, color=color.red)
geo_x_axis = arrow(pos=vector(0,0,0), axis=vector(3,0,0), color=color.white, shaftwidth=0.03, headwidth=.06, opacity = 0)
geo_y_axis = arrow(pos=vector(0,0,0), axis=vector(0,3,0), color=color.white, shaftwidth=0.03, headwidth=.06, opacity = 0)
geo_z_axis = arrow(pos=vector(0,0,0), axis=vector(0,0,3), color=color.white, shaftwidth=0.03, headwidth=.06, opacity = 0)
sun = distant_light(direction=(math.cos(solar_lon[0]*math.pi/180), math.sin(solar_lon[0]*math.pi/180), math.sin(solar_lat[0]*math.pi/180)), color=color.white)
spacecraft_position=curve(x=spacecraft_x, y=spacecraft_y, z=spacecraft_z)
x_label = label(pos=(3.1,0,0), text='x', visible=False)
y_label = label(pos=(0,3.1,0), text='y', visible=False)
z_label = label(pos=(0,0,3.1), text='z', visible=False)
sun_axis = arrow(pos=vector(0,0,0), axis=vector(3*math.cos(solar_lon[0]*math.pi/180), 3*math.sin(solar_lon[0]*math.pi/180), 3*math.sin(solar_lat[0]*math.pi/180)), color=color.yellow, shaftwidth=0.03, headwidth=.06, opacity = 0)


curve_list=[]
for i in range(1, len(mag_x)-1):
    curve_list.append(curve(x=[spacecraft_x[i], spacecraft_x[i]+mag_x[i]], y=[spacecraft_y[i], spacecraft_y[i]+mag_y[i]],z=[spacecraft_z[i], spacecraft_z[i]+mag_z[i]], visible=False))

#Every program needs to end with an infinite loop for some reason (that's what it says to do)
while True:
    rate(30)

