#!/usr/bin/env python2

import numpy as np
import sys
# import matplotlib.pyplot as plt

data = np.loadtxt(sys.argv[1], skiprows=1, delimiter=',')

# print data.shape

k = 0
n = 0
seq = []
R1 = ''
R1_data = []
pixel_vals = []
reg_dic = {
	1:'Transfer Serial data to buffers',
	2:'Write Debug Register',
	3:'Vertical Synchronal signal',
	4:'Write Configuration Register 1',
	5:'Read Configuration Register 1',
	6:'Write Configuration Register 2',
	7:'Read Configuration Register 2',
	8:'Write Configuration Register 3',
	9:'Read Configuration Register 3',
	10:'Write Configuration Register 4',
	11:'Read Configuration Register 4',
	12:'Enable All Output Channels',
	13:'Disable All Output Channels',
	14:'Pre-Active command'
}

for i in xrange(data.shape[0]):
	if data[i,3] == 1:
		if data[i,2] == 1:
			if data[i-1,2] == 0:
				k += 1
	elif data[i,3] == 0:
		if k > 1: # replace with k > 1 to remove 'Transfer Serial data to buffers' output
			print k, ':', reg_dic[k]
			seq.append(k)
		k = 0
	if (len(seq) > 3) and (len(seq) % 2 == 0) and (len(seq) < 13):
		if data[i,2] == 1:
			if data[i-1,2] == 0:
				R1 += str(int(data[i,1]))
				if len(R1) == 16:
					R1_data.append('0x'+format(int(R1, 2), '04X'))
					R1 = ''
					if len(R1_data) == 8:
						print 'data:', ','.join(R1_data) 
						R1_data = []
	if (len(seq) >= 13):
		if data[i,2] == 1:
			if data[i-1,2] == 0:
				R1 += str(int(data[i,1]))
				if len(R1) == 16:
					pixel_vals.append('0x'+format(int(R1, 2), '04X'))
					R1 = ''
					if len(pixel_vals) == 8:
						print 'num = ', str(n)+'\t', ','.join(pixel_vals)
						n += 1 
						pixel_vals = []

# np.savetxt('out.txt', data_diff, delimiter=',', fmt='%d')