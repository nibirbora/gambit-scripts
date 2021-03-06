# Gambit scripts
#
# Copyright (C) USC Information Sciences Institute
# Author: Nibir Bora <nbora@usc.edu>
# URL: <http://cbg.isi.edu/>
# For license information, see LICENSE

import os
import sys
import numpy
import matplotlib
import matplotlib.pyplot as plt

from matplotlib.ticker import FuncFormatter

import settings as my
sys.path.insert(0, os.path.abspath('..'))


#
# DISPLACEMENT FROM HOME - COMBINED PLOTS
#
DATA = {'all_days': {'hbk': (2.51862656908 , -0.784949777304),
					'south-la': (0.443342017512 , -0.584871677246),
					'west-la': (1.84785616418 , -0.752511521025),
					'south-bay': (1.90968037696 , -0.755235428729)},
		'weekdays': {'hbk': (5.29351309589 , -0.875495033521),
					'south-la': (0.446816556448 , -0.58491267971),
					'west-la': (2.39057082739 , -0.78488223198),
					'south-bay': (2.89477474957 , -0.807413173376)},
		'weekends': {'hbk': (0.65568123293 , -0.638785600777),
					'south-la': (0.54851373091 , -0.620647897449),
					'west-la': (1.25991614386 , -0.712834712369),
					'south-bay': (1.0458891347 , -0.688917748776)}}

REGIONS = ['hbk', 'south-la', 'west-la', 'south-bay']
'''COLORS = {'hbk': '#377EB8',
			'south-la' : '#FA71AF',
			'west-la' : '#4DAF4A',
			'south-bay' : '#A65628',
			'pomona' : '#3B3B3B',
			'bernardino' : '#984EA3',
			'riverside' : '#FF7F00'}'''
COLORS = {'hbk'		: 'b',
		'south-la' 	: 'm',
		'west-la' 	: 'g',
		'south-bay' : '#A65628'}
LINESTYLE = {'all_days': '-',
			'weekdays' : '--',
			'weekends' : '-.'}

RANGE = (100, 15000)

def out_disp_combined():
	'''Plot Power Law fits for regions on single plot'''
	a = 'all_days'
	wd = 'weekdays'
	we = 'weekends'
	h = 'hbk'
	s = 'south-la'
	w = 'west-la'
	b = 'south-bay'
	
	x = numpy.arange(RANGE[0], RANGE[1], 100)

	_plot(x, [(a,h), (a,s), (a,w), (a,b)], 'all_days_all_regions')
	_plot(x, [(wd,h), (wd,s), (wd,w), (wd,b)], 'weekdays_all_regions')
	_plot(x, [(we,h), (we,s), (we,w), (we,b)], 'weekends_all_regions')
	
	_plot(x, [(a,h), (wd,h), (we,h)], 'hbk')
	_plot(x, [(a,s), (wd,s), (we,s)], 'south-la')
	_plot(x, [(a,w), (wd,w), (we,w)], 'west-la')
	_plot(x, [(a,b), (wd,b), (we,b)], 'south-bay')

	_plot(x, [(a,h), (wd,h), (we,h), (a,s), (wd,s), (we,s), (a,w), (wd,w), (we,w), (a,b), (wd,b), (we,b)], 'all')
	

def _plot(x, Y, file_name):
	title = file_name.replace('_', ' ').upper()
	fig = plt.figure(figsize=(8,4))
	ax = fig.add_subplot(111)
	plt.subplots_adjust(left=0.075, right=0.96, top=0.92, bottom=0.08)
	#ax.set_autoscaley_on(False)
	#ax.set_ylim([0,0.1])
	ax.set_xlim(0, RANGE[1])
	
	powerlaw = lambda x, amp, index: amp * (x**index)
	for y in Y:
		day, region = y
		amp, index = DATA[day][region]
		label = '{region} ({day})'.format(day=day, region=region).upper()
		ax.plot(x, powerlaw(x, amp, index), label=label, linewidth=1, color=COLORS[region], alpha=0.95, linestyle=LINESTYLE[day])
	
	formatter = FuncFormatter(lambda v, pos: str(round(v*100, 2))+'%')
	plt.gca().yaxis.set_major_formatter(formatter)
	formatter = FuncFormatter(lambda v, pos: '' if v/1000 == 0 else str(int(v/1000))+'km')
	plt.gca().xaxis.set_major_formatter(formatter)
	ax.set_title(title, fontsize=11)
	ax.legend(fontsize=10)

	if not os.path.exists('data/' + my.DATA_FOLDER + 'disp_stat/'):
		os.makedirs('data/' + my.DATA_FOLDER + 'disp_stat/')
	plt.savefig('data/' + my.DATA_FOLDER + 'disp_stat/' + file_name + '.png')
	print 'Stored chart: %s' % file_name



