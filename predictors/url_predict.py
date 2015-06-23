import numpy as np
from scipy import stats
import h5py
import json
from StringIO import StringIO
import csv


def n_find_nearest(array,value,n):
  tmp = []
	
  for i in range(0, n):
	t = (np.abs(array-value)).argmin()
	tmp.append(t)
	array = np.delete(array,t,0)

  return tmp

    
url_result = []

def url_predit(bidder_req, bid):
	x = []
	y = []

	#shift time base on train_data['time'][0]
	time = []
	#print bids[bidder_id.translate(None, "[]'")]['req']['time']
	for t in bidder_req['time']:	
		ref = int(t - bidder_req['time'][0])
		time.append(ref)
	
	#print time[0]
	#unique url
	ref_url = np.unique(bidder_req['url']).tolist()	
    

	for i in range(0, len(time)):
	  x.append(time[i])
	  # define variant 
	  y.append(ref_url.index(str(bidder_req['url'][i]))+1)
	

	#generate linregress
	#slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
	slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)

	#search in url_class
	indexes = n_find_nearest(url_class[:,0], r_value ,10)
	#print indexes 

	c = 0
	for value in indexes:
		if ( url_class[value,1] == 1.0 ):
			c += 1


	print float(c)/float(len(indexes))
		 


	#url_result.append([ bid, url_class[idx,1]])
	#print url_class[idx][1]


url_ref = []
with open('url_model.json') as f:
	url_ref = json.load(f)
#print url_ref[1]
    
url_class = np.asarray(url_ref)
#url_class = np.unique(url_class)
b = np.ascontiguousarray(url_class).view(np.dtype((np.void, url_class.dtype.itemsize * url_class.shape[1])))
_, idx = np.unique(b, return_index=True)

url_class = url_class[idx]

#print url_class[:,0]


bids = h5py.File('bids_train.h5','r')

f = open('sampleSubmission.csv','r')
line = f.readline()

target_id = []
for line in f:
    values = np.genfromtxt(StringIO(line), dtype=([('bidder_id', 'a37'), ('prediction','f4')]), delimiter=',')
    values.shape = 1
    target_id.append(values['bidder_id'])



for bid in target_id:
	try:
		url_predit(bids[str(bid).translate(None, "[]'")]['req'], bid)
	except KeyError:
		url_result.append([str(bid), 0]) 






