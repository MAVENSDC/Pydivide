import pytplot
def tplot_varcreate(insitu):
	inst_list = ["EUV","LPW","STATIC","SWEA","SWIA","MAG","SEP","NGIMS"]
	for instrument in inst_list:
		for obs in insitu[instrument]:
			obs_specific = "mvn_kp::"+instrument.lower()+"::"+obs.lower()
			if insitu[instrument][obs].isnull().all() or insitu[instrument][obs].dtype == 'O':
				continue
			pytplot.store_data(obs_specific,data={'x':insitu['Time'], 'y': insitu[instrument][obs]})
