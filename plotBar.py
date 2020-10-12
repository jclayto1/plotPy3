import numpy as np
import argparse
import matplotlib.pyplot as plt

def _makeBarParser(argGroups):
	requiredGroup,fileArgsGroup,plotArgsGroup = argGroups
	plotArgsGroup.add_argument('-n','--numOfBin', type=int, help='number of bins in the histogram(s)', default=100)
	plotArgsGroup.add_argument('--norm', type=bool, help='if true, normalizes the histogram(s)',default=False)
	return

def plotHist(argParse,argGroups):
	"""
	Plots a histogram for a set of y values, given by --yCol. Default is to plot a histogram of the of the second column
	For additional help, use -h flag
	"""
	_makeBarParser(argGroups)
	requiredGroup,fileArgsGroup,plotArgsGroup = argGroups
	parser = argparse.ArgumentParser(parents=[argParse])
	argv = parser.parse_args()
	yVals = np.loadtxt(argv.filename, usecols=(argv.yCol))
	plt.hist(yVals, bins=argv.numOfBin, density=(argv.norm))
	return 
	
def plotMultiHist(argParse,argGroups):
	"""
	Plots a histogram for a set of y values (given by --yCol) taken from multiple files. Default is to plot a histogram of the of the second column
	For additional help, use -h flag
	"""
	_makeBarParser(argGroups)
	requiredGroup,fileArgsGroup,plotArgsGroup = argGroups
	requiredGroup.add_argument('filenames',type=str,nargs='+',help='additional files to plot')
	fileArgsGroup.add_argument('--yCol',type=int,nargs=1,help='index of the column containing y values (0 based, default=1)',default=1)
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
