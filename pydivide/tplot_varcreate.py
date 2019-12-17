# Copyright 2017 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pydivide

import pytplot


def tplot_varcreate(insitu, instruments=None, observations=None):
    """Creates tplot variables from the insitu variable
    """
    # initialize each instrument

    for obs in insitu["SPACECRAFT"]:
        obs_specific = "mvn_kp::spacecraft::" + obs.lower()
        try:
            pytplot.store_data(obs_specific, data={'x': insitu['Time'], 'y': insitu["SPACECRAFT"][obs]})
        except:
            pass

    created_vars = []
    inst_list = ["EUV", "LPW", "STATIC", "SWEA", "SWIA", "MAG", "SEP", "NGIMS"]
    for instrument in inst_list:
        if instruments is not None:
            if instrument not in instruments:
                continue
        # for each observation for each instrument
        if instrument in insitu:
            for obs in insitu[instrument]:
                if observations is not None:
                    if obs not in observations:
                        continue
                # create variable name
                obs_specific = "mvn_kp::" + instrument.lower() + "::" + obs.lower()
                try:
                    # store data in tplot variable
                    pytplot.store_data(obs_specific, data={'x': insitu['Time'], 'y': insitu[instrument][obs]})
                    pytplot.options(obs_specific, 'ytitle', '%s.%s' % (instrument, obs))
                    created_vars.append(obs_specific)
                    pytplot.link(obs_specific, "mvn_kp::spacecraft::altitude", link_type='alt')
                    pytplot.link(obs_specific, "mvn_kp::spacecraft::mso_x", link_type='x')
                    pytplot.link(obs_specific, "mvn_kp::spacecraft::mso_y", link_type='y')
                    pytplot.link(obs_specific, "mvn_kp::spacecraft::mso_z", link_type='z')
                    pytplot.link(obs_specific, "mvn_kp::spacecraft::geo_x", link_type='geo_x')
                    pytplot.link(obs_specific, "mvn_kp::spacecraft::geo_y", link_type='geo_y')
                    pytplot.link(obs_specific, "mvn_kp::spacecraft::geo_z", link_type='geo_z')
                    pytplot.link(obs_specific, "mvn_kp::spacecraft::sub_sc_longitude", link_type='lon')
                    pytplot.link(obs_specific, "mvn_kp::spacecraft::sub_sc_latitude", link_type='lat')
                except:
                    pass

    # Finally, link items to altitude
    obs_specific = "mvn_kp::spacecraft::altitude"
    pytplot.link(obs_specific, "mvn_kp::spacecraft::mso_x", link_type='x')
    pytplot.link(obs_specific, "mvn_kp::spacecraft::mso_y", link_type='y')
    pytplot.link(obs_specific, "mvn_kp::spacecraft::mso_z", link_type='z')
    pytplot.link(obs_specific, "mvn_kp::spacecraft::geo_x", link_type='geo_x')
    pytplot.link(obs_specific, "mvn_kp::spacecraft::geo_y", link_type='geo_y')
    pytplot.link(obs_specific, "mvn_kp::spacecraft::geo_z", link_type='geo_z')
    pytplot.link(obs_specific, "mvn_kp::spacecraft::sub_sc_longitude", link_type='lon')
    pytplot.link(obs_specific, "mvn_kp::spacecraft::sub_sc_latitude", link_type='lat')

    return created_vars