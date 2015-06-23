import numpy as np
from scipy import stats
import h5py
from StringIO import StringIO
import json


result = []

def url_behavior_model(bidder_req, outcome):
	
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
	  y.append( (ref_url.index(str(bidder_req['url'][i]))+1 )*100000000)



	#generate linregress
	#slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
	slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
	tmp = [r_value, float(outcome)]
	print tmp
	result.append(tmp)



bids = h5py.File('bids_train.h5','r')
f = open('train.csv','r')
line = f.readline()

train_set = []


for line in f:
    values = np.genfromtxt(StringIO(line), dtype=([('bidder_id', 'a37'), ('payment_account', 'a37'),('address','a37'),('outcome','f4')]), delimiter=',')
    values.shape = 1
    train_set.append(values)


for bid in train_set:
	try:
		url_behavior_model(bids[str(bid['bidder_id']).translate(None, "[]'")]['req'],bid['outcome'])
	except KeyError:
		print 'trash req' 

#print result
# result dump to JSON
with open('url_model.json', 'w') as outfile:
    json.dump(result, outfile)

