import pytplot
def tplot_varcreate(insitu):
	#initialize each instrument
	inst_list = ["EUV","LPW","STATIC","SWEA","SWIA","MAG","SEP","NGIMS"]
	for instrument in inst_list:
		#for each observation for each instrument
		for obs in insitu[instrument]:
			#create variable name
			obs_specific = "mvn_kp::"+instrument.lower()+"::"+obs.lower()
			#if NaN or string, continue
			if insitu[instrument][obs].isnull().all() or insitu[instrument][obs].dtype == 'O':
				continue
			#store data in tplot variable
			pytplot.store_data(obs_specific,data={'x':insitu['Time'], 'y': insitu[instrument][obs]})
