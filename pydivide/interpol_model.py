#There are 3 scenarios to interpolate:
#    1) MSO coordinate system with latitude/longitude/altitude 
#    2) GEO coordinate system with latitude/longitude/altitude 
#    3) MSO coordinate system with x/y/z
#NOTE: GEO x/y/z coordinate system is not allowed
#
#In all 3 cases, everything is converted to an MSO lat/lon/alt coordinate system.  
#For interpolation purposes, the atmosphere acts like a cube with dimensions lat*lon*alt
#This makes it so the interpolation is weighted more accurately.  
#A point that is 1 degree of lat/lon away will have as much influence as a point that is 1 kilometer higher or lower


import numpy as np
from pydivide.utilities import mvn_kp_sc_traj_xyz
from scipy import interpolate, spatial
from pydivide.read_model_results import read_model_results


def mvn_kp_interpol_model(kp,
                          model = None,
                          file = None,
                          nearest = False):
    
    print("This procedure was renamed, just use interpol_model")
    x = interpol_model(kp=kp,
                       model=model,
                       file=file,
                       nearest=nearest)
    return x
    
def interpol_model(kp,
                   model = None,
                   file = None,
                   nearest = False):
    
    if nearest:
        interp_method = 'nearest'
    else:
        interp_method = 'linear'
    
    if model==None and file==None:
        print("Please input either a model dictionary from read_model_results, or a model file.")
        return
    
    if file != None:
        model = read_model_results(file)
    
    model_interp = {}
    mars_radius = model['meta']['mars_radius']
    
    sc_mso_x = kp['SPACECRAFT']['MSO_X'].as_matrix()
    sc_mso_y = kp['SPACECRAFT']['MSO_Y'].as_matrix()
    sc_mso_z = kp['SPACECRAFT']['MSO_Z'].as_matrix()
    sc_path = np.array([sc_mso_x, sc_mso_y, sc_mso_z]).T


    
    if 'lon' in model['dim']:
        if 'mso' == model['meta']['coord_sys'].lower():     
            
            #Build a big matrix with dimensions 3 columns by (num lat * num lon * num alt) rows
            lat_mso_model = model['dim']['lat']
            lon_mso_model = model['dim']['lon']
            alt_mso_model = model['dim']['alt']
            
            lat_array = np.repeat(lat_mso_model, len(lon_mso_model))
            lon_array = np.tile(lon_mso_model, len(lat_mso_model))
            data_points = np.transpose(np.array([lon_array,lat_array]))
            index = 0
            for point in sc_path:
                r_mso = np.sqrt(point[0]**2 + point[1]**2 + point[2]**2)
                alt_mso = kp['SPACECRAFT']['ALTITUDE'][index]
                lat_mso = 90 - (np.arccos(point[2]/r_mso) / (np.pi / 180))
                lon_mso = np.arctan2(point[1], point[0]) / (np.pi / 180)
                sc_path[index] = np.array([lon_mso, lat_mso, alt_mso])
                index+=1
            
            latlon_triangulation = spatial.Delaunay(data_points)
            for var in model:
                if var.lower() == "geo_x":
                    continue
                if var.lower() == "geo_y":
                    continue
                if var.lower() == "geo_z":
                    continue
                print("Interpolating variable " + var)
                
                if var=='dim' or var=='meta':
                    continue
                #Rearrange the data to lon/lat/alt
                data = model[var]['data']
                dim_order_array = [0,1,2]
                for j in [0,1,2]:
                    if model[var]['dim_order'][j] == 'longitude':
                        dim_order_array[0] = j
                    elif model[var]['dim_order'][j] == 'latitude':
                        dim_order_array[1] = j
                    elif model[var]['dim_order'][j] == 'altitude':
                        dim_order_array[2] = j
                data_new = np.transpose(data, dim_order_array)
                
                #Build an array of values that correspond to the points in data point
                values = np.empty([len(lat_mso_model)*len(lon_mso_model), len(alt_mso_model)])
                index = 0 
                for alt in range(0,len(alt_mso_model)):
                    for lat in range(0,len(lat_mso_model)):
                        for lon in range(0,len(lon_mso_model)):
                            values[index, alt] = data_new[lon][lat][alt]           
                            index+=1
                    index = 0
                    
                x = np.empty(len(sc_path))
                index = 0
                for sc_pos in sc_path:
                    if sc_pos[2] > np.max(alt_mso_model):
                        x[index] = np.NaN
                        index+=1
                        continue
                    if sc_pos[2] < np.min(alt_mso_model):
                        x[index] = np.NaN
                        index+=1
                        continue
                    sorted_x_distance = np.argsort(np.abs(alt_mso_model-sc_pos[2]))
                    alti1=sorted_x_distance[0]
                    if nearest:
                        x[index] = interpolate.griddata(data_points, values[:,alti1], [sc_pos[0], sc_pos[1]], method='nearest')
                    else:
                        if alt_mso_model[alti1] < sc_pos[2]:
                            alti2=alti1+1
                        else:
                            temp = alti1 -1
                            alti2 = alti1
                            alti1 = temp
                        #Interpolate through space
                        first_val_calc = interpolate.LinearNDInterpolator(latlon_triangulation, values[:,alti1])
                        second_val_calc = interpolate.LinearNDInterpolator(latlon_triangulation, values[:,alti2])
                        first_val = first_val_calc([sc_pos[0], sc_pos[1]])
                        second_val = second_val_calc([sc_pos[0], sc_pos[1]])
                        delta_1 = sc_pos[2] - alt_mso_model[alti1]
                        delta_2 = alt_mso_model[alti2] - sc_pos[2]
                        delta_tot = alt_mso_model[alti2] - alt_mso_model[alti1]
                        x[index] = ((first_val*delta_2) + (second_val*delta_1)) / (delta_tot)
                    index+=1
                model_interp[var] = np.array(x)
                
        if 'geo' == model['meta']['coord_sys'].lower():            
            #Build the Matrix that transforms GEO to MSO coordinates 
            ls_rad = model['meta']['ls'] * np.pi / 180
            rads_tilted_y = 25.19 * np.sin(ls_rad) * np.pi / 180
            rads_tilted_x = -25.19 * np.cos(ls_rad) * np.pi / 180
            lonsubsol_rad = -model['meta']['longsubsol'] * np.pi / 180
            
            z_rotation = np.matrix([[np.cos(lonsubsol_rad), -np.sin(lonsubsol_rad), 0],
                                   [np.sin(lonsubsol_rad), np.cos(lonsubsol_rad), 0],
                                   [0, 0, 1]])
            y_rotation = np.matrix([[np.cos(rads_tilted_y), 0, np.sin(rads_tilted_y)],
                                   [0, 1, 0],
                                   [-np.sin(rads_tilted_y), 0, np.cos(rads_tilted_y)]])
            x_rotation = np.matrix([[1, 0, 0],
                                   [0, np.cos(rads_tilted_x), -np.sin(rads_tilted_x)],
                                   [0, np.sin(rads_tilted_x), np.cos(rads_tilted_x)]]) 
            geo_to_mso_matrix = np.dot(x_rotation, np.dot(y_rotation, z_rotation))
            
            
            #Build a big matrix with dimensions 3 columns by (num lat * num lon * num alt) rows
            lat_geo_model = model['dim']['lat']
            lon_geo_model = model['dim']['lon']
            alt_geo_model = model['dim']['alt']
            
            alt_array = np.repeat(alt_geo_model, len(lon_geo_model)*len(lat_geo_model))
            lat_array = np.tile(np.repeat(lat_geo_model, len(lon_geo_model)), len(alt_geo_model))
            lon_array = np.tile(lon_geo_model, len(lat_geo_model)*len(alt_geo_model))
            data_points = np.transpose(np.array([lon_array,lat_array,alt_array]))
            
            #Convert to GEO coordinates, then to MSO
            index = 0
            for point in data_points:
                r = point[2] + mars_radius
                x = r * np.sin((90 - point[1]) * np.pi / 180) * np.cos(point[0] * np.pi / 180)
                y = r * np.sin((90 - point[1]) * np.pi / 180) * np.sin(point[0] * np.pi / 180)
                z = r * np.cos((90 - point[1]) * np.pi / 180)
                data_points[index] = np.dot(geo_to_mso_matrix, np.array([x,y,z]))
                index+=1
            
            #Convert to MSO Lon/Lat/Alt in order to weight the interpolation better
            lat_mso = np.empty(len(lon_geo_model)*len(lat_geo_model))
            lon_mso = np.empty(len(lon_geo_model)*len(lat_geo_model))
            index = 0
            for point in data_points:
                r_mso = np.sqrt(point[0]**2 + point[1]**2 + point[2]**2)
                lat_mso[index] = 90 - (np.arccos(point[2]/r_mso) / (np.pi / 180))
                lon_mso[index] = np.arctan2(point[1], point[0]) / (np.pi / 180)
                index+=1
                if index >= len(lon_geo_model)*len(lat_geo_model):
                    break
            latlon_points = np.transpose(np.array([lon_mso,lat_mso]))
             
            index = 0
            for point in sc_path:
                r_mso = np.sqrt(point[0]**2 + point[1]**2 + point[2]**2)
                alt_mso = kp['SPACECRAFT']['ALTITUDE'][index]
                lat_mso = 90 - (np.arccos(point[2]/r_mso) / (np.pi / 180))
                lon_mso = np.arctan2(point[1], point[0]) / (np.pi / 180)
                sc_path[index] = np.array([lon_mso, lat_mso, alt_mso])
                index+=1
                
            latlon_triangulation = spatial.Delaunay(latlon_points)
            #Loop through the variables in the model
            for var in model:
                if var.lower() == "geo_x":
                    continue
                if var.lower() == "geo_y":
                    continue
                if var.lower() == "geo_z":
                    continue
                if var=='dim' or var=='meta':
                    continue
                print("Interpolating variable " + var)
                #Rearrange the data to lon/lat/alt
                data = model[var]['data']
                dim_order_array = [0,1,2]
                for j in [0,1,2]:
                    if model[var]['dim_order'][j] == 'longitude':
                        dim_order_array[0] = j
                    elif model[var]['dim_order'][j] == 'latitude':
                        dim_order_array[1] = j
                    elif model[var]['dim_order'][j] == 'altitude':
                        dim_order_array[2] = j
                data_new = np.transpose(data, dim_order_array)
                
                #Build an array of values that correspond to the points in data point
                values = np.empty([len(lat_geo_model)*len(lon_geo_model), len(alt_geo_model)])
                index = 0 
                for alt in range(0,len(alt_geo_model)):
                    for lat in range(0,len(lat_geo_model)):
                        for lon in range(0,len(lon_geo_model)):
                            values[index, alt] = data_new[lon][lat][alt]              
                            index+=1
                    index = 0
                    
                    
                x = np.empty(len(sc_path))
                index = 0
                for sc_pos in sc_path:
                    if sc_pos[2] > np.max(alt_geo_model):
                        x[index] = np.NaN
                        index+=1
                        continue
                    if sc_pos[2] < np.min(alt_geo_model):
                        x[index] = np.NaN
                        index+=1
                        continue
                    sorted_x_distance = np.argsort(np.abs(alt_geo_model-sc_pos[2]))
                    alti1=sorted_x_distance[0]
                    if nearest:
                        x[index] = interpolate.griddata(latlon_points, values[:,alti1], [sc_pos[0], sc_pos[1]], method='nearest')
                    else:
                        if alt_geo_model[alti1] < sc_pos[2]:
                            alti2=alti1+1
                        else:
                            temp = alti1 -1
                            alti2 = alti1
                            alti1 = temp
                        #Interpolate through space
                        first_val_calc = interpolate.LinearNDInterpolator(latlon_triangulation, values[:,alti1])
                        second_val_calc = interpolate.LinearNDInterpolator(latlon_triangulation, values[:,alti2])
                        first_val = first_val_calc([sc_pos[0], sc_pos[1]])
                        second_val = second_val_calc([sc_pos[0], sc_pos[1]])
                        delta_1 = sc_pos[2] - alt_geo_model[alti1]
                        delta_2 = alt_geo_model[alti2] - sc_pos[2]
                        delta_tot = alt_geo_model[alti2] - alt_geo_model[alti1]
                        x[index] = ((first_val*delta_2) + (second_val*delta_1)) / (delta_tot)
                    index+=1
                model_interp[var] = np.array(x)
                
    else:
        if 'mso' == model['meta']['coord_sys'].lower():   
            #Build a big matrix with dimensions 3 columns by (num lat * num lon * num alt) rows
            x_mso_model = model['dim']['x']
            y_mso_model = model['dim']['y']
            z_mso_model = model['dim']['z']            
            
            #Loop through the variables in the model
            for var in model:
                if var.lower() == "geo_x":
                    continue
                if var.lower() == "geo_y":
                    continue
                if var.lower() == "geo_z":
                    continue
                
                if var=='dim' or var=='meta':
                    continue
                #Rearrange the data to lon/lat/alt
                data = model[var]['data']
                dim_order_array = [0,1,2]
                for j in [0,1,2]:
                    if model[var]['dim_order'][j] == 'x':
                        dim_order_array[0] = j
                    elif model[var]['dim_order'][j] == 'y':
                        dim_order_array[1] = j
                    elif model[var]['dim_order'][j] == 'z':
                        dim_order_array[2] = j
                data_new = np.transpose(data, dim_order_array)
                
                #Interpolate through space
                model_interp[var] = mvn_kp_sc_traj_xyz(x_mso_model, y_mso_model, z_mso_model, data_new, sc_mso_x, sc_mso_y, sc_mso_z, nn=interp_method)
            
    return model_interp