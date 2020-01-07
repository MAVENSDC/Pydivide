Getting Started
=================



System Requirements
-------------------

The MAVEN PyDIVIDE toolkit currently requires Anaconda 5.0 or above.
Anaconda will install Python, as well as numerous software libraries for scientific
computing. This toolkit is only compatible with Python 3.5 or above.

To install the PyDIVIDE toolkit, type the following command into the local
terminal/Anaconda Prompt terminal.

	pip install pydivide
	
This will automatically install most of the required dependencies.  The following is necessary for the Bokeh HTML plots:

	conda install -c bokeh nodejs

And finally, though this is not required, for 3D visualization you will need to get PyOpenGL

	pip install pyopengl


The PyDIVIDE toolkit can also be downloaded from the MAVEN Science
Data Center GitHub page, https://github.com/MAVENSDC. This will require
manual installation of all dependencies of PyDIVIDE. It is recommended that
PyDIVIDE be installed via the pip command above.


Updating the Toolkit
---------------------

The latest version of PyDIVIDE can be installed by typing the following command
into the terminal ::

	pip install pydivide --upgrade
	

Running PyDIVIDE
-----------------

An IDE is the recommended way to run PyDIVIDE procedures; however, they
can also be run from the terminal. To start an interactive session of Python,
enter the following commands into the terminal ::

	ipython
	import pydivide

Data Storage
-------------

PyDIVIDE requires all data files to be stored in an automatically-created directory
structure.  This has a similar format to the
SDC and SSL directory structures.  The root directory for data storage can be
chosen by the user.  When first running a download_files or read procedure,
the user will be prompted to select the root_data_dir. After the directory
is selected, it is saved in mvn_toolkit_prefs.txt, and can later be changed
manually as desired. After the first selection of the directory, the user will not
be prompted by download_files or read again. download_files will place
files into the chosen directory structure, and read will pull data files from that 
directory structure.

.. note::
	If you have pyspedas installed (installed by default when installed via pip), then pydivide
	will use the pyspedas data directory.  The default is C://Datapy, but can be changed with 
	pyspedas.set_prefs('data_dir', '/insert/path/for/your/data')

While you do not necessarily need to know this to use the toolkit, the data directories are 
structured as such

	<root_data_dir>/maven/data/sci
								/kp/insitu/YYYY/MM/
								/kp/iuvs/YYYY/MM/
								/sta/l2/YYYY/MM/
								/sep/l2/YYYY/MM/
								/swi/l2/YYYY/MM/
								/swe/l2/YYYY/MM/
								/lpw/l2/YYYY/MM/
								/mag/l2/YYYY/MM/
								/iuv/l2/YYYY/MM/
								/ngi/l2/YYYY/MM/
								/euv/l2/YYYY/MM/
								/acc/l2/YYYY/MM/
