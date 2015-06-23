# from scipy import stats
# import numpy as np
# x = np.random.random(1000)
# #print x
# y = np.random.random(1000)
# slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)

# print slope, r_value, p_value
import h5py
import numpy as np

def group_event(target_id):
	grp = w.create_group(target_id)
	print target_id
	tmp = []
	#print type(list(w))
	for bid in bids:
		if ( target_id == str(bid['bidder_id'])):
			#print '!!!'
			tmp.append(bid)
	print 'in function len of tmp: ' + str(len(tmp))
	grp['req'] = tmp
	#return tmp
	
			

w = h5py.File('bids_train.h5','w')
f = h5py.File('bids.h5','r')

dset = f['bids']
bids = dset[...]
#bids.tolist()

print 'here'
for i in range(1,7656335):
  #print 'len of: ' + str(len(bids))
  print 'loop:'+ str(i)+' ' + bids[i]['bidder_id']
  if (str(bids[i]['bidder_id']) in list(w)):
  	continue
  group_event(str(bids[i]['bidder_id']))
  #print 'len of tarsh: '+ str(len(trash))
  #bids = np.delete(bids, trash, 0 )

w.close()
