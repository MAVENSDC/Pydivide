import pydivide

def fullplot(instruments=None,
             level='l2',
             type=None,
             start_date='2014-01-01',
             end_date='2014-01-02',
             tplot_names='',
             filenames=None,
             insitu=None,
             parameter=''):
    '''
    Plot any insitu Level 2 or KP data from MAVEN.  Downloads files found into PySPEDAS and loads them into memory via PyTplot.
    Then creates an interactive plot window including spectrogram slicer, MAVEN's location and orbit in MSO coordinates, and MAVEN's
    location in GEO coordinates, especially relative to the crustal magnetic fields.

    Parameters:
        instruments: str/list of str
            Instruments from which you want to download data.
            Accepted values are any combination of: sta, swi, swe, lpw, euv, ngi, iuv, mag, sep, rse
        type: str/list of str
            The observation/file type of the instruments to load.  If None, all file types are loaded.
            Otherwise, a file will only be loaded into tplot if its descriptor matches one of the strings in this field.
            See the instrument SIS for more detail on types.
            Accepted values are:
                =================== ====================================
                Instrument           Level 2 Observation Type/File Type
                =================== ====================================
                EUV                 bands
                LPW                 lpiv, lpnt, mrgscpot, we12, we12burstlf, we12bursthf, we12burstmf, wn, wspecact, wspecpas
                STATIC              2a, c0, c2, c4, c6, c8, ca, cc, cd, ce, cf, d0, d1, d4, d6, d7, d8, d9, da, db
                SEP                 s1-raw-svy-full, s1-cal-svy-full, s2-raw-svy-full, s2-cal-svy-full
                SWEA                coarsearc3d, coarsesvy3d, finearc3d, finesvy3d, onboardsvymom, onboardsvyspec
                SWIA                arc3d, arcpad, svy3d, svypad, svyspec
                MAG                 ss, pc, pl, ss1s, pc1s, pl1s
                =================== =====================================
        tplot_names : list of str
            The tplot names to plot.  Also not needed, use only if the variables are already loaded into memory.
        filenames: str/list of str ['yyyy-mm-dd']
            List of files to load
        start_date: str
            String that is the start date for downloading data (YYYY-MM-DD), or the orbit number
        end_date: str
            String that is the end date for downloading data (YYYY-MM-DD), or the orbit number
        kp : dict
            insitu kp data structure/dictionary read from file(s).  This is not required, only needed if you want to plot
            variables from this data structure.
        parameter : list of str/int
            If the above kp data structure is given, this variable will be the parameters to plot (see the pydivide.plot function)
    Returns :
        None

    Examples:
        >>> # Plots EUV Bands, LPW LP-IV, and MAG SS data on Jan 01 2015
        >>> pydivide.fullplot(instruments=['euv', 'lpw', 'mag'], type=['bands', 'lpiv', 'ss1s'], start_date='2015-01-01', end_date='2015-01-02')
    '''
    import os
    import pyspedas
    import pytplot
    from pyqtgraph.Qt import QtCore, QtGui

    if insitu != None:
        pydivide.plot(insitu, parameter=parameter, exec_qt=False)
        pytplot.options('mvn_kp::spacecraft::altitude', 'map', 1)
        map_file = os.path.join(os.path.dirname(__file__), 'basemaps', 'MAG_Connerny_2005.jpg')
        pytplot.options('mvn_kp::spacecraft::altitude', 'basemap', map_file)
        pytplot.tplot('mvn_kp::spacecraft::altitude', exec_qt=False, window_name='PYDIVIDE_MAP2D', pos_2d=True, pos_3d=True)
    elif tplot_names == '':
        tplot_names = pyspedas.maven_load(filenames=filenames, instruments=instruments, level=level, type=type, start_date=start_date, end_date=end_date)
        pytplot.options('mvn_kp::spacecraft::altitude', 'map', 1)
        map_file = os.path.join(os.path.dirname(__file__), 'basemaps', 'MAG_Connerny_2005.jpg')
        pytplot.options('mvn_kp::spacecraft::altitude', 'basemap', map_file)
        pytplot.tplot(tplot_names, pos_2d=True, pos_3d=True, interactive=True, exec_qt=False, window_name='PYDIVIDE_PLOT')
        pytplot.tplot('mvn_kp::spacecraft::altitude', exec_qt=False, window_name='PYDIVIDE_MAP2D', extra_functions=[],
                      extra_function_args=[])
    else:
        pytplot.options('mvn_kp::spacecraft::altitude', 'map', 1)
        map_file = os.path.join(os.path.dirname(__file__), 'basemaps', 'MAG_Connerny_2005.jpg')
        pytplot.options('mvn_kp::spacecraft::altitude', 'basemap', map_file)
        pytplot.tplot(tplot_names, pos_2d=True, pos_3d=True, interactive=True, exec_qt=False, window_name='PYDIVIDE_PLOT')
        pytplot.tplot('mvn_kp::spacecraft::altitude', exec_qt=False, window_name='PYDIVIDE_MAP2D', extra_functions=[],
                      extra_function_args=[])



    app = QtGui.QApplication([])
    win = QtGui.QMainWindow()
    app.setStyle("Fusion")

    plot_splitter = QtGui.QSplitter(QtCore.Qt.Vertical, frameShape=QtGui.QFrame.StyledPanel,
                                    frameShadow=QtGui.QFrame.Plain)
    ancillary_splitter = QtGui.QSplitter(QtCore.Qt.Vertical, frameShape=QtGui.QFrame.StyledPanel,
                                         frameShadow=QtGui.QFrame.Plain)
    main_splitter = QtGui.QSplitter(QtCore.Qt.Horizontal, frameShape=QtGui.QFrame.StyledPanel,
                                    frameShadow=QtGui.QFrame.Plain)
    main_splitter.addWidget(plot_splitter)
    main_splitter.addWidget(ancillary_splitter)

    for i, plot_name in enumerate(pytplot.pytplotWindow_names):
        if plot_name == 'PYDIVIDE_PLOT':
            plot_splitter.addWidget(pytplot.pytplotWindows[i])

    for i, plot_name in enumerate(pytplot.pytplotWindow_names):
        if plot_name == 'PYDIVIDE_MAP2D':
            plot_splitter.addWidget(pytplot.pytplotWindows[i])

    for i, plot_name in enumerate(pytplot.pytplotWindow_names):
        if plot_name == 'Spec_Slice':
            ancillary_splitter.addWidget(pytplot.pytplotWindows[i])
    for i, plot_name in enumerate(pytplot.pytplotWindow_names):
        if plot_name == '2D_MARS':
            ancillary_splitter.addWidget(pytplot.pytplotWindows[i])
    for i, plot_name in enumerate(pytplot.pytplotWindow_names):
        if plot_name == '3D_MARS':
            ancillary_splitter.addWidget(pytplot.pytplotWindows[i])

    main_splitter.show()


    #This section will be for implementing IUVS KP data
    '''    
    import pyqtgraph.opengl as gl
    iuvs_data = gl.GLLinePlotItem()
    for i, plot_name in enumerate(pytplot.pytplotWindow_names):
        if plot_name == '3D_MARS':
            pytplot.pytplotWindows[i].centralWidget().addItem(iuvs_data)
            
    import math
    insitu, iuvs = pydivide.read(input_time='2016-02-18')
    time = iuvs[0]['periapse1']['time_start']
    lat = np.radians(90 - iuvs[0]['periapse1']['lat'])
    lon = np.radians(iuvs[0]['periapse1']['lon'])
    alt = np.array(iuvs[0]['periapse1']['density']['ALTITUDE']) + 3389.5
    # determine transformation matrix
    time = pytplot.tplot_utilities.str_to_int(time)
    iuvs_time = np.abs(insitu['Time'].values - time).argmin()
    print(iuvs_time)
    rotmat = np.array([[insitu['SPACECRAFT']['T11'][iuvs_time], insitu['SPACECRAFT']['T12'][iuvs_time],
                        insitu['SPACECRAFT']['T13'][iuvs_time]],
                       [insitu['SPACECRAFT']['T21'][iuvs_time], insitu['SPACECRAFT']['T22'][iuvs_time],
                        insitu['SPACECRAFT']['T23'][iuvs_time]],
                       [insitu['SPACECRAFT']['T31'][iuvs_time], insitu['SPACECRAFT']['T32'][iuvs_time],
                        insitu['SPACECRAFT']['T33'][iuvs_time]]])
    
    mso_coords = []
    for a in alt:
        x = math.cos(lat) * math.cos(lon) * a
        y = math.cos(lat) * math.sin(lon) * a
        z = math.sin(lat) * a
    
        mso_coords.append(np.matmul(rotmat, np.array([x,y,z])))
    
    mso_coords = np.array(mso_coords)
    print(mso_coords)
    iuvs_data.setData(pos=mso_coords, width=10)
    '''


    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        app.exec_()