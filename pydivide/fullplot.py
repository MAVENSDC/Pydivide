from .utilities import get_inst_obs_labels, param_list, orbit_time
import builtins
import pydivide

def fullplot(insitu=None,
             iuvs=None,
             tplot_names='',
             filenames=None,
             instruments=None,
             level='l2',
             type=None,
             start_date='2014-01-01',
             end_date='2014-01-02',
             parameter=''):

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