While in graduate school I wrote a series of CLI plotting tools to help quickly visualize columns in various datafiles. As these grew (and as I became more comfortable with python) I refactored the collection of code into a single CLI tool. I started this goal around the python2 end of life announcement, hence I named the tool plotPy3.

# Usage
`python3 plotPy3.py help`

```
General purpose plotting script, designed to give a quick and simple plot for a space delimited file often created MD engines and analysis packages. This script depends upon matplotlib (plot creation) and numpy (file reading, data manipulation). 

Usage: python plotPy3 [command] [args]

Available commands:
-------------------
	help		Print this message
	plot		Plots one or more columns from a file
	multi		Plots a column from multiple files
	hist		Plots a histogram of one or more columns from a file
	multihist	Plots a histogram of a column from multiple files
	heat    	Plots a heatmap from three columns in a file
	matrix		Plots a MxN heatmap from a file with M rows and N columns
	hist2d  	Plots a 2D histogram from two columns in a file
To see available arguments, run 'python plotPy3 [command] -h'

Examples:
---------
Plot the RMSD of a domain vs. time from cpptraj
	python plotPy3 plot rmsdFile.dat -x 'Frames' -y 'RMSD ($\AA$)' -l 'Domain 1'

Plot the RMSD of two domains vs. time with 100 ps per frame stride
	python plotPy3 plot rmsdFile.dat --yCol 1 2 --xScale 0.1 -x 'Simulation time (ns)' -y 'RMSD ($\AA$)' -l 'Domain 1' 'Domain 2'

Plot a CV from colvars module in NAMD from three separate simulations
	python plotPy3 multi sim1.colvars.traj sim2.colvars.traj sim3.colvars.traj -x 'Step number' -y 'CV value' -l 'Simulation 1' 'Simulation 2' 'Simulation 3'

```

# Dependencies
Any recent version of matplotlib and numpy.
