# Copyright 2017 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pydivide

##########
pydivide
##########

Pydivide is a python package which allows the user to quickly plot MAVEN key parameter data.  This toolkit uses the "pytplot" library.     

Pydivide can be used in python scripts, or interactively through IPython and the Jupyter notebook.  

Install Python
=============

You will need the Anaconda distribution of Python 3 in order to run pytplot.  

`Anaconda <https://www.continuum.io/downloads/>`_ comes with a suite of packages that are useful for data science. 


Install pydivide
=============

Open up a terminal, and type::

	pip install pydivide
	
This will install pydivide and all of it's dependencies.  

You will also need to install nodejs.  This can be done through Anaconda with the following command::

	conda install -c bokeh nodejs

Running Pydivide
=============

To start using pytplot in a similar manner to IDL tplot, start up an interactive environment through the terminal command::

	ipython 
	
or, if you prefer the jupyter interactive notebook::

	jupyter notebook
	
then, just import the package by typing the command::

	import pydivide

A demo/tutorial can be found here: `docs/pytplot_tutorial.html <http://htmlpreview.github.com/?https://github.com/MAVENSDC/Pydivide/blob/master/docs/pydivide_tutorial.html>`_.
	
	
Contact
=============

If you have any suggestions or notice any problems, don't hesitate to contact Bryan Harter: harter@lasp.colorado.edu 