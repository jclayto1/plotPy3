import numpy as np
import matplotlib.pyplot as plt
import argparse

def _makeHeatParser(argGroups):
	"""
	Helper function to add parameters used by each heatplot function (for example, colorbar limits)
	Takes a list of argument groups (assumed to be [requiredGroup,fileArgsGroup,plotArgsGroup]
	"""
	requiredGroup,fileArgsGroup,plotArgsGroup = argGroups
	plotArgsGroup.add_argument('--heatmap', type=str, help='heatmap coloring')
	plotArgsGroup.add_argument('--zmin', type=float, help='minimum z value to be displayed (exclusive)', default=None)
	plotArgsGroup.add_argument('--zmax', type=float, help='maximum z value to be displayed (inclusive)', default=None)
	plotArgsGroup.add_argument('-z','--zlabel', type=str, help='colorbar label', default='')
	return

def _loadMatrix(filename,args):
	#Load columns from file
	xvals = np.loadtxt(filename, usecols=(args.xCol))
	yvals = np.loadtxt(filename, usecols=(args.yCol))
	zvals = np.loadtxt(filename, usecols=(args.zCol))

	#Extract unique values
	xAxis = np.unique(xvals)
	yAxis = np.unique(yvals)
	
	#Create matrix 
	xlength = len(xAxis)
	ylength = len(yAxis)
	matrix = np.zeros([ylength,xlength])			#[row,col]
	for i in range(0,xlength):
		for j in range (0,ylength):
			matrix[j][i] = zvals[j+i*ylength]	#File iterates over y values, then x
		
	return np.flipud(matrix), xAxis, yAxis			#Flip needed because [0,0] occurs at (x[0], y[-1])

def plotHeat(argParse,argGroups):
	_makeHeatParser(argGroups)
	required,fileArgs,plotArgs = argGroups
	fileArgs.add_argument('--zCol',type=int,nargs=1,help='index of the column containing z values (0 based, default=2)',default=2)
	plotArgs.add_argument('--discardZero', type=bool, help='hides bins with a count of zero', default=False)
	plotArgs.add_argument('--useRelative', type=bool, help='Sets the minimum value to zero and scales accordingly',default=False)
	parser = argparse.ArgumentParser(parents=[argParse])
	argv = parser.parse_args()
	filename = argv.filename

	xCol = argv.xCol
	yCol = argv.yCol

	#Read data
	matrix,xVals,yVals = _loadMatrix(filename, argv)

	if (argv.discardZero):
		matrix[matrix==0] = np.nan

	#Plot data
	x_binSize = (xVals[1] - xVals[0])
	y_binSize = (yVals[1] - yVals[0])
	limits = [np.min(xVals)-x_binSize/2.,np.max(xVals)+x_binSize/2.,np.min(yVals)-y_binSize/2.,np.max(yVals)+y_binSize/2.]

	#Resize minimum if desired
	if (argv.useRelative):
		matrix -= np.amin(matrix)
	plt.imshow(matrix, interpolation='nearest', extent=limits, aspect='auto', cmap=argv.heatmap, vmin=argv.zmin, vmax=argv.zmax)

	#Show titles (defaults '')
	plt.colorbar().set_label(argv.zlabel)
	if(argv.xLim is not None): plt.xlim(argv.xLim)
	if(argv.yLim is not None): plt.ylim(argv.yLim)

def plotMatrix(argParse,argGroups):
	_makeHeatParser(argGroups)
	parser = argparse.ArgumentParser(parents=[argParse])
	argv = parser.parse_args()
	matrix = np.loadtxt(argv.filename) 
	plt.imshow(matrix,origin='lower',aspect='auto',cmap=argv.heatmap,vmin=argv.zmin,vmax=argv.zmax)
	plt.gca().xaxis.tick_bottom()
	plt.colorbar().set_label(argv.zlabel)
	return

def plotHist2d(argParse,argGroups):
	_makeHeatParser(argGroups)
	required,fileArgs,plotArgs = argGroups
	fileArgs.add_argument('--yCol',type=int,nargs=1,help='index of the column containing y values (0 based, default=1)',default=1)
	plotArgs.add_argument('--nBins',type=int,help='Number of bins (applied to both diminsions)',default=25)
	plotArgs.add_argument('--discardZero', type=bool, help='hides bins with a count of zero', default=False)
	parser = argparse.ArgumentParser(parents=[argParse],conflict_handler='resolve')
	argv = parser.parse_args()
	val1, val2 = np.loadtxt(argv.filename, usecols=(argv.xCol,argv.yCol),unpack=True)
	cMin = 0.0
	if(argv.discardZero):
		cMin = 1e-8
	plt.hist2d(val1,val2,bins=argv.nBins,vmin=argv.zmin,vmax=argv.zmax,cmin=cMin)
	plt.gca().xaxis.tick_bottom()
	plt.colorbar().set_label(argv.zlabel)
	return
