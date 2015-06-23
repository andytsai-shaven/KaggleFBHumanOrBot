import numpy as np
from scipy import stats
import h5py
from StringIO import StringIO
import json
from url_predict
from req_predict

##load file

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
		url_predict(bids[str(bid).translate(None, "[]'")]['req'], bid)
		req_predict(bids[str(bid).translate(None, "[]'")]['req'], bid)
	except KeyError:
		print 'trash req' 


#each model would generate a probability 
with open('ans.csv', 'w') as ans_file:
    csvwriter = csv.writer(ans_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow(['bidder_id', 'prediction'])
    
    for i in range(0, len(url_result)):
    	prediction = url_result[i][1] + req_result[i][1]
    	csvwriter.writerow([url_result[i][0], prediction])
    	









