Introduction
===================



What is pytplot?
------------------

Pytplot is an effort by the Laboratory for Atmospheric and Space Physics to replicate the functionality IDL tplot library.  
It is a tool for manipulating, analyzing, and plotting time series data.  Primarily, it is focused on handling lines 
and spectrograms from satellite data.  It can plot using either Qt via pytqtgraph, or using HTML files via Bokeh.  


What does it do?
-------------------

Because the tplot library evolved over several decades with new features being added depending on what scientists needed, 
there is a variety of things it does:

* Reads in data from a variety of sources (including netCDF and CDF file readers)
* Stores data in a common format, alongside all of its metadata and plot options.
* Plots the data in a stacked time series plot with time as the common axis.
* Easily add new axes 
* Provides a list of simple commands to modify the plots (line styles, colors, etc), or overplot two different variables
* Provides time series data analysis/manipulation routines
* Provides tools to enable mouse interactions with other python routines

Pyqtgraph Sample
-----------------

.. image:: _images/sample.png


Interactive Bokeh Sample
------------------------

.. raw:: html
   :file: _images/sample.html
   
   
Version History
---------------

1.4.7 Changes:

* Added two more ancillary plots, Mars 2D Map and Mars 3D Map

1.4.6 Changes:

* Occasionally logged spec plots would not be properly displayed, this is a hopefully a quick fix for that

1.4.5 Changes:

* Fixing typescript errors with bokeh

1.4.4 Changes:

* Fixing pyqtgraph's collections.abc imports

1.4.3 Changes:

* Bug fix where ylog could not be unset

1.4.1 Changes:

* Fixed small bug in the spec plots for certain file types
* Added PySPEDAS changes to the cdf_to_tplot routine

1.4.0 Changes:

* Added documentation
* Redid tplot variables as xarrays
* Added many unit tests
* Numerous bug fixes

1.3.3 Changes:

* Added power spectrum calculation routine

1.3.2 Changes:

* Updates to the spectrogram plots and CDF reader

1.3.0 Changes:

* Added interactive plots for spectrograms, documentation coming soon

1.2.11 Changes:

* Commenting out tplot_math stuff

1.2.9 Changes:

* Added a netcdf_to_tplot reader
* Changed date axis to show more relevant times

1.2.8 Changes:

* Adding merge functionality to the cdf_to_tplot routine

1.2.5 Changes:

* Adding tplot_math, with various basic functions to begin data analysis
* Crosshairs now implemented in pyqtgraph
* Timebars work in alt/map plots

1.2.4 Changes:

* Fixed for latest version of Anaconda

1.2.1 Changes:

* Fixed a bug in the pyqtgraph spec plots with time varying bins

1.2.0 Changes:

* Added ability to display an arbitrarily large number of qt plot windows, if done from ipython

1.1.13 Changes:

* Added overplot capabilities to the Qt Plotting routines

1.1.12 Changes:

* Fixed major issue with pip installer
* Added ability to use pytplot without a graphics interface, if building only html files are desired.

1.1.6 Changes:

* Fixed a spot where python warnings were changed to change back after the function was over

1.1.4 Changes:

* Added a qt option to tplot, which will allow users to just open the HTML file in a browser window

1.1.3 Changes:

* Bug fix, pyqtgraph was creating a layout every time which eventually caused a crash
* Still a known error where bokeh will no longer plot more than once

1.1.2 Changes:

* Added support for bokeh 0.12.13

1.1.0 Changes:

* Added the ability to plot directly in the Qt Window with pyqtgraph.  This may entirely replace the bokeh plotting routines at some point.

1.0.15 Changes:

* Changing tplot to use QtWebKitWidgets by default, but attempt to use QWebEngineView if not found

1.0.14 Changes:

* Fixed a bug in cdf_to_tplot

1.0.11 Changes:

* Bug fixes in the last couple of revisions

1.0.8 Changes:

* Reverting back QWebEngineView changes from 1.0.6

1.0.7 Changes:

* Should be able to export to HTML properly now.

1.0.6 Changes:

* Qt is getting rid of support for QtWebView.  QWebEngineView will replace it, but has great difficulty viewing html greater than 2GB.
* As a temporary solution, a local html file is saved, and then read into QWebEngineView.

1.0.5 Changes:

* Fixed a memory leak

1.0.2 Changes:

* Added cdf_to_tplot routine
* Made a version checker