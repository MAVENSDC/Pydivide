import numpy as np
import scipy
import os
from pydivide.mvn_kp_utilities import mvn_kp_sc_traj_xyz
from scipy import interpolate, spatial
from pydivide.mvn_kp_read_model_results import mvn_kp_read_model_results

def mvn_kp_create_model_maps(altitude,
                             model=None,
                             file=None,
                             numContours=25,
                             fill=False,
                             ct='jet',  # https://matplotlib.org/examples/color/colormaps_reference.html
                             transparency=1,
                             nearest=False,
                             linear=True):
    import matplotlib
    matplotlib.use('tkagg')
    import matplotlib.pyplot as plt
    
    
    if model==None and file==None:
        print("Please input either a model or the file path/name to a model.")
        return
    if file != None:
        model = mvn_kp_read_model_results(file)
    
    
    print("Select a variable to plot: ")
    index=0
    name_index_dict = {}
    for name in model:
        if name.lower() == 'dim':
            continue
        if name.lower() == 'meta':
            continue
        print(index, ": ", name)
        name_index_dict[index] = name
        index+=1
    i_choice=int(input("Enter Selection: "))
    dataname=name_index_dict[i_choice].lower()
    
    mars_radius = model['meta']['mars_radius']
    lats = np.arange(181)-90
    lons = np.arange(361)-180
    sc_lat_mso = np.repeat(lats, len(lons))
    sc_lon_mso = np.tile(lons, len(lats))
    r = np.full(len(sc_lon_mso), altitude+mars_radius)
    sc_alt_array = np.full(len(sc_lon_mso), altitude)
    sc_mso_x = r * np.sin((90-sc_lat_mso)*(np.pi/180)) * np.cos(sc_lon_mso*(np.pi/180))
    sc_mso_y = r * np.sin((90-sc_lat_mso)*(np.pi/180)) * np.sin(sc_lon_mso*(np.pi/180))
    sc_mso_z = r * np.cos((90-sc_lat_mso)*(np.pi/180))
    sc_path = np.array([sc_mso_x, sc_mso_y, sc_mso_z]).T
                  
    if nearest:
        interp_method = 'nearest'
    else:
        interp_method = 'linear'
    
    if model==None and file==None:
        print("Please input either a model dictionary from mvn_kp_read_model_results, or a model file.")
        return
    
    
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
                alt_mso = altitude
                lat_mso = 90 - (np.arccos(point[2]/r_mso) / (np.pi / 180))
                lon_mso = np.arctan2(point[1], point[0]) / (np.pi / 180)
                sc_path[index] = np.array([lon_mso, lat_mso, alt_mso])
                index+=1
            
            latlon_triangulation = spatial.Delaunay(data_points)
            for var in model:
                if var.lower() != dataname:
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
                tracer = np.array(x)
                
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
                alt_mso = altitude
                lat_mso = 90 - (np.arccos(point[2]/r_mso) / (np.pi / 180))
                lon_mso = np.arctan2(point[1], point[0]) / (np.pi / 180)
                sc_path[index] = np.array([lon_mso, lat_mso, alt_mso])
                index+=1
                
            latlon_triangulation = spatial.Delaunay(latlon_points)
            #Loop through the variables in the model
            for var in model:
                if var.lower() != dataname:
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
                tracer = np.array(x)
                
    else:
        if 'mso' == model['meta']['coord_sys'].lower():   
            #Build a big matrix with dimensions 3 columns by (num lat * num lon * num alt) rows
            x_mso_model = model['dim']['x']
            y_mso_model = model['dim']['y']
            z_mso_model = model['dim']['z']            
            
            #Loop through the variables in the model
            for var in model:
                if var.lower() != dataname:
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
                tracer = mvn_kp_sc_traj_xyz(x_mso_model, y_mso_model, z_mso_model, data_new, sc_mso_x, sc_mso_y, sc_mso_z, nn=interp_method)
    
    
    xi, yi = np.linspace(sc_lon_mso.min(), sc_lon_mso.max(), 300), np.linspace(sc_lat_mso.min(), sc_lat_mso.max(), 300)
    xi, yi = np.meshgrid(xi, yi)
    zi = scipy.interpolate.griddata((sc_lon_mso, sc_lat_mso), tracer, (xi, yi), method=interp_method)
    fig=plt.figure()
    ax = fig.add_subplot(1,1,1)
    if fill:
        plt.contourf(xi, yi, zi, numContours, alpha=transparency, cmap=ct, extent=(-180,-90,180,90))
    else:
        CS = plt.contour(xi, yi, zi, numContours, alpha=transparency, cmap=ct)
        plt.clabel(CS, inline=1, fontsize=7, fmt='%1.0f')
    extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    plt.axis('off')
    save_name = "ModelData_"+dataname+"_"+str(altitude)+"km"
    if fill:
        save_name = save_name + "_filled"
    plt.savefig(os.path.join(os.path.dirname(file),save_name+".png"), transparent=False, bbox_inches=extent, pad_inches=0, dpi=150)
    plt.show()
    