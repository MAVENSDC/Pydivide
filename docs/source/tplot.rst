Key Parameters to Tplot Variables
==================================

PyDIVIDE ultimately uses PyTplot to do plotting routines.  If you would prefer to work with the KP data in PyTplot directly, then this is the function for you. 


.. autofunction:: pydivide.tplot_varcreate


The variables created are stored in a global dictionary of xarray objects, and given names in the form ::

	mvn::kp::{instrument}::{observation}

For example: "mvn::kp::mag::mso_x"