import numpy as np
import argparse
import matplotlib.pyplot as plt


def _makeLineParser(argGroups):
	"""
	Helper function to add parameters used by each line-plot function (for example, the style of the line)
	Takes a list of argument groups (assumed to be [requiredGroup,fileArgsGroup,plotArgsGroup]
	"""
	requiredGroup,fileArgsGroup,plotArgsGroup = argGroups
#	requiredGroup.add_argument('filename',type=str, help='filename of the file to plot')
	plotArgsGroup.add_argument('--style', type=str, help='style of the plotted line; applies to each line drawn', choices=['solid','dashed','dashdot','dotted'],default='solid')
	
def _plot(xVals,yVals,argv,Label=None):
	"""
	Helper function for plotting a line with an optional legend
	"""
	if Label is None:
		plt.plot(xVals*argv.xScale,yVals*argv.yScale,linestyle=argv.style)	
	else:
		plt.plot(xVals*argv.xScale,yVals*argv.yScale,label=Label,linestyle=argv.style)
		plt.legend(loc=argv.legendLoc)

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
	if isinstance(yvals[0], float):
		try:
			_plot(xvals,yvals,argv,argv.labels[0])
		except:
			_plot(xvals,yvals,argv)

	#Case: multiple columns of yvals
	else:
		for i,yval in enumerate(yvals):
			try:
				_plot(xvals,yval,argv,argv.labels[i])
			except:
				_plot(xvals,yval,argv)

	#Change axis to values
	if argv.yLim is not None:
		plt.ylim(argv.yLim)
	if argv.xLim is not None:
		plt.xlim(argv.xLim)
	return argv

def plotMultiFile(argParse,argGroups):
	"""
	Plots two columns (y vs x) from a given list of files. Default settings plot the second column vs the first column
	For additional help, use -h flag
	"""
	#Parameters from user
	_makeLineParser(argGroups)
	requiredGroup,fileArgsGroup,plotArgsGroup = argGroups
	requiredGroup.add_argument('filenames',type=str,nargs='+',help='additional files to plot')
	fileArgsGroup.add_argument('--yCol',type=int,nargs=1,help='index of the column containing y values (0 based, default=1)',default=1)
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
		if argv.labels is None:
			_plot(xvals,yvals,argv)
		else:
			_plot(xvals,yvals,argv,Label=argv.labels[fileindex])
	#Show titles (defaults '')
	if (argv.xLim is not None): plt.xlim(argv.xLim)
	if (argv.yLim is not None): plt.ylim(argv.yLim)
	return argv

def plotHist(argParse,argGroups):
	"""
	Plots a histogram for a set of y values, given by --yCol. Default is to plot a histogram of the of the second column
	For additional help, use -h flag
	"""
	_makeLineParser(argGroups)
	requiredGroup,fileArgsGroup,plotArgsGroup = argGroups
	plotArgsGroup.add_argument('-n','--numOfBin', type=int, help='number of bins in the histogram(s)', default=100)
	plotArgsGroup.add_argument('--norm', type=bool, help='if true, normalizes the histogram(s)',default=False)
	parser = argparse.ArgumentParser(parents=[argParse])
	argv = parser.parse_args()
	yVals = np.loadtxt(argv.filename, usecols=(argv.yCol))
	plt.hist(yVals, bins=argv.numOfBin, density=(argv.norm))
	return argv
	
def plotMultiHist(argParse,argGroups):
	"""
	Plots a histogram for a set of y values (given by --yCol) taken from multiple files. Default is to plot a histogram of the of the second column
	For additional help, use -h flag
	"""
	_makeLineParser(argGroups)
	requiredGroup,fileArgsGroup,plotArgsGroup = argGroups
	requiredGroup.add_argument('filenames',type=str,nargs='+',help='additional files to plot')
	fileArgsGroup.add_argument('--yCol',type=int,nargs=1,help='index of the column containing y values (0 based, default=1)',default=1)
	plotArgsGroup.add_argument('-n','--numOfBin', type=int, help='number of bins in the histogram(s)', default=100)
	plotArgsGroup.add_argument('--norm', type=bool, help='if true, normalizes the histogram(s)',default=False)
	plotArgsGroup.add_argument('--separate', type=bool, help='if true, treats the files as separate data sets',default=False)
	plotArgsGroup.add_argument('--histtype',type=str,help='style of the histogram (default=bar)',default='bar')
	parser = argparse.ArgumentParser(parents=[argParse],conflict_handler='resolve')
	argv = parser.parse_args()
	argv.filenames.insert(0,argv.filename)
	
	yVals = np.array([])
	if(argv.separate): 
		yVals = [np.loadtxt(filename,usecols=(argv.yCol)) for filename in argv.filenames]
	else:
		for filename in argv.filenames:
			yVals = np.concatenate((yVals,np.loadtxt(filename,usecols=(argv.yCol))))
	if(argv.labels is None):
		plt.hist(yVals, bins=argv.numOfBin, density=(argv.norm),histtype=argv.histtype)
	else:
		plt.hist(yVals, bins=argv.numOfBin, density=(argv.norm),histtype=argv.histtype,label=argv.labels)
		plt.legend()
	return argv
