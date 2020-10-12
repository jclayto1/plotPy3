#!/home/josephclayton/anaconda3/bin/python3

"""
General purpose plotting script, designed to give a quick and simple plot for a space delimited file often created MD engines and analysis packages. This script depends upon matplotlib (plot creation) and numpy (file reading, data manipulation). 

Usage: python plotPy3 [command] [args]

Available commands:
-------------------
	help	Print this message
	plot	Plots one or more columns from a file
	multi	Plots a column from multiple files
	heat    Plots a heatmap from three columns in a file
	matrix	Plots a MxN heatmap from a file with M rows and N columns
	heat2d  Plots a 2D histogram from two columns in a file
To see available arguments, run 'python plotPy3 [command] -h'

Examples:
---------
Plot the RMSD of a domain vs. time from cpptraj
	python plotPy3 plot rmsdFile.dat -x 'Frames' -y 'RMSD ($\AA$)' -l 'Domain 1'

Plot the RMSD of two domains vs. time with 100 ps per frame stride
	python plotPy3 plot rmsdFile.dat --yCol 1 2 --xScale 0.1 -x 'Simulation time (ns)' -y 'RMSD ($\AA$)' -l 'Domain 1' 'Domain 2'

Plot a CV from colvars module in NAMD from three separate simulations
	python plotPy3 multi sim1.colvars.traj sim2.colvars.traj sim3.colvars.traj -x 'Step number' -y 'CV value' -l 'Simulation 1' 'Simulation 2' 'Simulation 3'

"""
#"print" is a function in Python 3, but many in the lab run in Python 2.
#Once everyone moves on from the past, this import will not be needed.
from __future__ import print_function

import argparse
import sys
from plotLines import *
from plotHeat import *

def _printHelp():
	print(__doc__)
	sys.exit()
def printHelp(parser,groups):
	_printHelp()

#Implemented functions
commands = {'help': printHelp,
	'plot':plotFile,
	'multi':plotMultiFile,
	'heat':plotHeat,
	'matrix':plotMatrix,
	'hist':plotHist,
	'multihist':plotMultiHist,
	'hist2d':plotHist2d}
#Print usage
if (len(sys.argv)<2): _printHelp()
if (sys.argv[1]=='help'): _printHelp()

#Create parent argparser
parentPrs = argparse.ArgumentParser(add_help=False,conflict_handler='resolve')
requiredGroup = parentPrs.add_argument_group('required')
fileArgsGroup = parentPrs.add_argument_group('file arguments')
plotArgsGroup    = parentPrs.add_argument_group('plotting arguments')

requiredGroup.add_argument('command', type=str,choices=commands.keys())
requiredGroup.add_argument('filename',type=str, nargs='?', help='filename of the file to plot')
fileArgsGroup.add_argument('--xCol', type=int, nargs=1, help='index of the column containing x values (0 based, default=0)', default=[0,])
fileArgsGroup.add_argument('--yCol', type=int, nargs='+', help='index of the column containing y values (0 based, default=1); can accept multiple values', default=[1,])
plotArgsGroup.add_argument('--xScale', type=float, help='scaling factor for x values', default=1.0)
plotArgsGroup.add_argument('--yScale', type=float, help='scaling factor for y values', default=1.0)
plotArgsGroup.add_argument('-t','--title', type=str, help='title of figure', default='')
plotArgsGroup.add_argument('-x','--xlabel', type=str, help='x-axis label', default='')
plotArgsGroup.add_argument('-y','--ylabel', type=str, help='y-axis label', default='')
plotArgsGroup.add_argument('-l','--labels', type=str, nargs='+', help='column labels for legend')
plotArgsGroup.add_argument('--legendLoc', type=str, help='sets location of the legend (used only if -l or --labels is given)', choices=['right','center left','upper right','lower right','best','center','lower left','center right','upper left','upper center','lower center'], default='upper right')
plotArgsGroup.add_argument('--yLim',type=float, nargs=2, help='y-axis limits. Given as min max',default=None)
plotArgsGroup.add_argument('--xLim',type=float, nargs=2, help='x-axis limits. Given as min max',default=None)
plotArgsGroup.add_argument('--figSize',type=float, nargs=2, help='size of figure in inches. Given as width height', default=(6.4,4.8))
plotArgsGroup.add_argument('--rcstyle',type=str, help='Style to use; see matplotlib.pyplot.style.use for more information',default='default')
#Pass argparser and argument groups to desired function
argGroups = [requiredGroup,fileArgsGroup,plotArgsGroup]
argv,unknown=parentPrs.parse_known_args()
try:
	plt.style.use(argv.rcstyle)
	currFig = plt.figure(figsize=argv.figSize)
	parser = commands[sys.argv[1]](parentPrs,argGroups)
	#TO DO: have function prepare a matplotlib figure, then do labeling/showing here
	#Plt is loaded in the command function
	plt.title(argv.title)
	plt.xlabel(argv.xlabel)
	plt.ylabel(argv.ylabel)
	if(argv.xLim is not None): plt.xlim(argv.xLim)
	if(argv.yLim is not None): plt.ylim(argv.yLim)
	plt.show()

except KeyError as e:
	print("Error: command '%s' not implemented."%sys.argv[1])
	print("Current implemented commands:")
	[print(key) for key in commands.keys()]
except:
	raise
