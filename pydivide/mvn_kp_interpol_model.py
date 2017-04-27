import numpy as np
from scipy import interpolate
from pydivide.mvn_kp_read_model_results import mvn_kp_read_model_results

def mvn_kp_interpol_model(kp,
                          model = None,
                          model_file = None,
                          nearest = False):
    
    if nearest:
        interp_method = 'nearest'
    else:
        interp_method = 'linear'
    
    if model==None and model_file==None:
        print("Please input either a model dictionary from mvn_kp_read_model_results, or a model file.")
        return
    
    if model_file != None:
        model = mvn_kp_read_model_results(model_file)
    
    model_interp = {}
    mars_radius = model['meta']['mars_radius']
    
    sc_mso_x = kp['SPACECRAFT']['MSO X'].as_matrix()
    sc_mso_y = kp['SPACECRAFT']['MSO Y'].as_matrix()
    sc_mso_z = kp['SPACECRAFT']['MSO Z'].as_matrix()
    sc_path = np.array([sc_mso_x, sc_mso_y, sc_mso_z]).T
    
    
    if 'lon' in model['dim']:
        if 'mso' == model['meta']['coord_sys'].lower():     
            
            #Build a big matrix with dimensions 3 columns by (num lat * num lon * num alt) rows
            lat_mso_model = model['dim']['lat']
            lon_mso_model = model['dim']['lon']
            alt_mso_model = model['dim']['alt']
            
            lon_array = np.repeat(lon_mso_model, len(alt_mso_model)*len(lat_mso_model))
            lat_array = np.tile(np.repeat(lat_mso_model, len(alt_mso_model)), len(lon_mso_model))
            alt_array = np.tile(alt_mso_model, len(lat_mso_model)*len(lon_mso_model))
            data_points = np.transpose(np.array([lon_array,lat_array,alt_array]))
               
            for var in model:
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
                values = np.empty(len(data_points))
                index = 0 
                for i in range(0,len(lon_mso_model)):
                    for j in range(0,len(lat_mso_model)):
                        for k in range(0,len(alt_mso_model)):
                            values[index] = data_new[i][j][k]              
                            index+=1
                
                index = 0
                for point in sc_path:
                    r_mso = np.sqrt(point[0]**2 + point[1]**2 + point[2]**2)
                    alt_mso = r_mso - mars_radius
                    lat_mso = 90 - (np.arccos(point[2]/r_mso) / (np.pi / 180))
                    lon_mso = np.arctan2(point[0], point[1]) / (np.pi / 180)
                    sc_path[index] = np.array([lon_mso, lat_mso, alt_mso])
                    index+=1
                
                #Interpolate through space
                model_interp[var] = interpolate.griddata(data_points, values, sc_path, method=interp_method)
        
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
            
            lon_array = np.repeat(lon_geo_model, len(alt_geo_model)*len(lat_geo_model))
            lat_array = np.tile(np.repeat(lat_geo_model, len(alt_geo_model)), len(lon_geo_model))
            alt_array = np.tile(alt_geo_model, len(lat_geo_model)*len(lon_geo_model))
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
            index = 0
            for point in data_points:
                r_mso = np.sqrt(point[0]**2 + point[1]**2 + point[2]**2)
                alt_mso = r_mso - mars_radius
                lat_mso = 90 - (np.arccos(point[2]/r_mso) / (np.pi / 180))
                lon_mso = np.arctan2(point[0], point[1]) / (np.pi / 180)
                data_points[index] = np.array([lon_mso, lat_mso, alt_mso])
                index+=1
                
            index = 0
            for point in sc_path:
                r_mso = np.sqrt(point[0]**2 + point[1]**2 + point[2]**2)
                alt_mso = r_mso - mars_radius
                lat_mso = 90 - (np.arccos(point[2]/r_mso) / (np.pi / 180))
                lon_mso = np.arctan2(point[0], point[1]) / (np.pi / 180)
                sc_path[index] = np.array([lon_mso, lat_mso, alt_mso])
                index+=1
                
                
            #Loop through the variables in the model
            for var in model:
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
                values = np.empty(len(data_points))
                index = 0 
                for i in range(0,len(lon_geo_model)):
                    for j in range(0,len(lat_geo_model)):
                        for k in range(0,len(alt_geo_model)):
                            values[index] = data_new[i][j][k]              
                            index+=1
                #Interpolate through space
                model_interp[var] = interpolate.griddata(data_points, values, sc_path, method=interp_method)
                
    else:
        if 'mso' == model['meta']['coord_sys'].lower():   
            #Build a big matrix with dimensions 3 columns by (num lat * num lon * num alt) rows
            x_mso_model = model['dim']['x']
            y_mso_model = model['dim']['y']
            z_mso_model = model['dim']['z']
            
            x_array = np.repeat(x_mso_model, len(z_mso_model)*len(x_mso_model))
            y_array = np.tile(np.repeat(y_mso_model, len(z_mso_model)), len(x_mso_model))
            z_array = np.tile(z_mso_model, len(x_mso_model)*len(y_mso_model))
            data_points = np.transpose(np.array([x_array,y_array,z_array]))
            
            #Get the path of the spacecraft
            sc_mso_x = kp['SPACECRAFT']['MSO X'].as_matrix()
            sc_mso_y = kp['SPACECRAFT']['MSO Y'].as_matrix()
            sc_mso_z = kp['SPACECRAFT']['MSO Z'].as_matrix()
            sc_path = np.array([sc_mso_x, sc_mso_y, sc_mso_z]).T
            
            #Convert to MSO Lon/Lat/Alt in order to weight the interpolation better
            index = 0
            for point in data_points:
                r_mso = np.sqrt(point[0]**2 + point[1]**2 + point[2]**2)
                alt_mso = r_mso - mars_radius
                lat_mso = 90 - (np.arccos(point[2]/r_mso) / (np.pi / 180))
                lon_mso = np.arctan2(point[0], point[1]) / (np.pi / 180)
                data_points[index] = np.array([lon_mso, lat_mso, alt_mso])
                index+=1
                
            index = 0
            for point in sc_path:
                r_mso = np.sqrt(point[0]**2 + point[1]**2 + point[2]**2)
                alt_mso = r_mso - mars_radius
                lat_mso = 90 - (np.arccos(point[2]/r_mso) / (np.pi / 180))
                lon_mso = np.arctan2(point[0], point[1]) / (np.pi / 180)
                sc_path[index] = np.array([lon_mso, lat_mso, alt_mso])
                index+=1
            
            
            #Loop through the variables in the model
            for var in model:
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
                
                #Build an array of values that correspond to the points in data point
                values = np.empty(len(data_points))
                index = 0 
                for i in range(0,len(x_mso_model)):
                    for j in range(0,len(y_mso_model)):
                        for k in range(0,len(z_mso_model)):
                            values[index] = data_new[i][j][k]              
                            index+=1
                
                #Interpolate through space
                model_interp[var] = interpolate.griddata(data_points, values, sc_path, method=interp_method)
        
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
            x_geo_model = model['dim']['x']
            y_geo_model = model['dim']['y']
            z_geo_model = model['dim']['z']
            
            x_array = np.repeat(x_geo_model, len(z_geo_model)*len(x_geo_model))
            y_array = np.tile(np.repeat(y_geo_model, len(z_geo_model)), len(x_geo_model))
            z_array = np.tile(z_mso_model, len(x_geo_model)*len(y_geo_model))
            data_points = np.transpose(np.array([x_array,y_array,z_array]))
            
            #Convert to MSO x,y,z
            index = 0
            for point in data_points:
                data_points[index] = np.dot(geo_to_mso_matrix, np.array([point[0],point[1],point[2]]))
                index+=1
            
            #Get the path of the spacecraft
            sc_mso_x = kp['SPACECRAFT']['MSO X'].as_matrix()
            sc_mso_y = kp['SPACECRAFT']['MSO Y'].as_matrix()
            sc_mso_z = kp['SPACECRAFT']['MSO Z'].as_matrix()
            sc_path = np.array([sc_mso_x, sc_mso_y, sc_mso_z]).T
            
            
            #Convert to MSO Lon/Lat/Alt in order to weight the interpolation better
            index = 0
            for point in data_points:
                r_mso = np.sqrt(point[0]**2 + point[1]**2 + point[2]**2)
                alt_mso = r_mso - mars_radius
                lat_mso = 90 - (np.arccos(point[2]/r_mso) / (np.pi / 180))
                lon_mso = np.arctan2(point[0], point[1]) / (np.pi / 180)
                data_points[index] = np.array([lon_mso, lat_mso, alt_mso])
                index+=1
                
            index = 0
            for point in sc_path:
                r_mso = np.sqrt(point[0]**2 + point[1]**2 + point[2]**2)
                alt_mso = r_mso - mars_radius
                lat_mso = 90 - (np.arccos(point[2]/r_mso) / (np.pi / 180))
                lon_mso = np.arctan2(point[0], point[1]) / (np.pi / 180)
                sc_path[index] = np.array([lon_mso, lat_mso, alt_mso])
                index+=1
            
            #Loop through the variables in the model
            for var in model:
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
                
                #Build an array of values that correspond to the points in data point
                values = np.empty(len(data_points))
                index = 0 
                for i in range(0,len(x_geo_model)):
                    for j in range(0,len(y_geo_model)):
                        for k in range(0,len(z_geo_model)):
                            values[index] = data_new[i][j][k]              
                            index+=1                
                #Interpolate through space
                model_interp[var] = interpolate.griddata(data_points, values, sc_path, method=interp_method)
            
    return model_interp