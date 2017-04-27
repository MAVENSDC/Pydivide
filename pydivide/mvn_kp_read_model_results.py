import netCDF4
import math 

#Takes in a .nc file from the MAVEN website and reads it into python dictionary
#results
#    \_ meta ()
#        \_ longsubsol
#        \_ ls
#        \_ etc
#    \_ dim
#        \_ lat/x
#        \_ lon/y
#        \_ alt/z
#    \_ variable1
#        \_ dim_order (x,y,z or z,y,x for example)
#        \_ data
#    \_ variable2
#        \_ dim_order
#        \_ data
#    ...
#    \_ variableN


def mvn_kp_read_model_results(file):
    
    
    #Create dictionaries for the metadata and dimensions
    meta = {}
    dim = {}
    
    #Create a dictionary for the above dictionaries
    results = {}
    
    
    model = netCDF4.Dataset(file, "r+", format="NETCDF4")
    lat_size = None
    lon_size = None
    alt_size = None
    x_size = None
    y_size = None
    z_size = None 
    
    for unit in model.dimensions:
        if unit.lower() == 'latitude':
            lat_size = model.dimensions[unit].size
        if unit.lower() == 'longitude':
            lon_size = model.dimensions[unit].size
        if unit.lower() == 'altitude':
            alt_size = model.dimensions[unit].size
        if unit.lower() == 'size_x' or unit.lower() == 'x':
            x_size = model.dimensions[unit].size   
        if unit.lower() == 'size_y' or unit.lower() == 'y':
            y_size = model.dimensions[unit].size 
        if unit.lower() == 'size_z' or unit.lower() == 'z':
            z_size = model.dimensions[unit].size    
            
    if lat_size != None:
        if (lon_size == None) or (alt_size == None):
            print("Couldn't find all dimensions: LATITUDE,LONGITUDE,ALTITUDE")
        dimension_type = "latlonalt"
    elif x_size != None:
        if (y_size == None) or (z_size == None):
            print("Couldn't find all dimensions: X,Y,Z")
        dimension_type = "xyz"
    else:
        print("Problem finding either cartesian (X,Y,Z) or Lat Lon Alt dimensions")
        return
    
    for var in model.variables:
        if var.lower() == 'latitude':
            dim['lat'] = model.variables[var][0:lat_size]
        elif var.lower() == 'longitude':
            dim['lon'] = model.variables[var][0:lon_size]    
        elif var.lower() == 'altitude':
            dim['alt'] = model.variables[var][0:alt_size]
        elif var.lower() == 'x':
            dim['x'] = model.variables[var][0:x_size]
        elif var.lower() == 'y':
            dim['y'] = model.variables[var][0:y_size]
        elif var.lower() == 'z':
            dim['z'] = model.variables[var][0:z_size]
        elif var.lower() == 'coordinate_system':
            meta['coord_sys'] = model.variables[var][0]
        elif var.lower() == 'ls':
            if abs(model.variables[var][0]) >= 2*math.pi:
                meta['ls'] = model.variables[var][0]
            else:
                if 'units' in model.variables[var].__dict__:
                    if model.variables[var].__dict__['units'].lower == 'rad':
                        meta['ls'] = math.degrees(model.variables[var][0])
                    else:
                        meta['ls'] = model.variables[var][0]
                else:
                    meta['ls'] = model.variables[var][0]
        elif var.lower() == 'longsubsol':
            if abs(model.variables[var][0]) >= 2*math.pi:
                meta['longsubsol'] = model.variables[var][0]
            else:
                if 'units' in model.variables[var].__dict__:
                    if model.variables[var].__dict__['units'].lower == 'rad':
                        meta['longsubsol'] = math.degrees(model.variables[var][0])
                    else:
                        meta['longsubsol'] = model.variables[var][0]
                else:
                    meta['longsubsol'] = model.variables[var][0]
        elif var.lower() == 'dec':
            if abs(model.variables[var][0]) >= 2*math.pi:
                meta['dec'] = model.variables[var][0]
            else:
                if 'units' in model.variables[var].__dict__:
                    if model.variables[var].__dict__['units'].lower == 'rad':
                        meta['dec'] = math.degrees(model.variables[var][0])
                    else:
                        meta['dec'] = model.variables[var][0]
                else:
                    meta['dec'] = model.variables[var][0]
        elif var.lower() == 'mars_radius':
            meta['mars_radius'] = model.variables[var][0] 
        elif var.lower() == 'altitude_from':
            meta['altitude_from'] = model.variables[var][0]
        else:
            if (len(model.variables[var].shape) == 3) or (len(model.variables[var].shape) == 4):
                data = {}
                if model.variables[var].units == 'm-3':
                    value = model.variables[var][:]/1000000.0
                else:
                    value = model.variables[var][:]
                dim_order = model.variables[var].dimensions
                data['data'] = value
                data['dim_order'] = dim_order
                results[var] = data
    
    #Create a dictionary of dictionaries for the model results
    results['meta'] = meta
    results['dim'] = dim
    
    return results