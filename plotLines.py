import numpy as np
import argparse
import matplotlib.pyplot as plt


def _makeLineParser(argGroups):
	"""
	Helper function to add parameters used by each line-plot function (for example, the style of the line)
	Takes a list of argument groups (assumed to be [requiredGroup,fileArgsGroup,plotArgsGroup])
	"""
	requiredGroup,fileArgsGroup,plotArgsGroup = argGroups
	plotArgsGroup.add_argument('--style', type=str, help='style of the plotted line; applies to each line drawn', choices=['solid','dashed','dashdot','dotted'],default='solid')
	return	

def _plot(xVals,yVals,argv):
	"""
	Helper function for plotting a line
	"""
	plt.plot(xVals[::argv.stride]*argv.xScale,yVals[::argv.stride]*argv.yScale,linestyle=argv.style)

def plotFile(argParse,argGroups):
	"""
	Plots two columns (y vs x) from a given file. Default settings plot the second column vs the first column
	For additional help, use -h flag
	"""
	#Parameters from user
	_makeLineParser(argGroups) 
	parser = argparse.ArgumentParser(parents=[argParse])
	argv = parser.parse_args()

	filename = argv.filename
	xCol = argv.xCol
	yCol = argv.yCol

	#Read data
	xvals = np.loadtxt(filename, usecols=(xCol))
	yvals = np.loadtxt(filename, usecols=(yCol)).transpose()  #This is needed to plot columns separately

	#Plot data
	#Case: only one column of yvals
	if(len(yvals.shape)==1):
		_plot(xvals,yvals,argv)

	#Case: multiple columns of yvals
	else:
		for i,yval in enumerate(yvals):	
			_plot(xvals,yval,argv)

	#Change axis to values
	if(argv.yLim is not None):
		plt.ylim(argv.yLim)
	if(argv.xLim is not None):
		plt.xlim(argv.xLim)
	return 

def plotMultiFile(argParse,argGroups):
	"""
	Plots two columns (y vs x) from a given list of files. Default settings plot the second column vs the first column
	For additional help, use -h flag
	"""
	#Parameters from user
	_makeLineParser(argGroups)
	requiredGroup,fileArgsGroup,plotArgsGroup = argGroups
	requiredGroup.add_argument('filenames',type=str,nargs='+',help='additional files to plot')
	fileArgsGroup.add_argument('--yCol',type=int,help='index of the column containing y values (0 based, default=1)',default=1)
	parser = argparse.ArgumentParser(parents=[argParse],conflict_handler='resolve')
	argv = parser.parse_args()
	xCol = argv.xCol
	yCol = argv.yCol

	#Loop over files
	argv.filenames.insert(0,argv.filename)				#Argv.filename is a required argument, argv.filenames follow after
	for fileindex,filename in enumerate(argv.filenames):
		#Read data
		xvals = np.loadtxt(filename, usecols=(xCol))
		yvals = np.loadtxt(filename, usecols=(yCol)).transpose()  #This is needed to plot columns separately

		#Plot data
		_plot(xvals,yvals,argv)
	#Show titles 
	if (argv.xLim is not None): plt.xlim(argv.xLim)
	if (argv.yLim is not None): plt.ylim(argv.yLim)
	return 
