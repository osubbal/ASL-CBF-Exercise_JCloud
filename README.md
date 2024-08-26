# About

- Related Publication: []

## 01 - Image Processing
- Coding Language: bash
- Required Software:
	- FSL
		- BASIL
	- FreeSurfer

## 02 - Analysis and Visualization
- Coding Language: Python
- Version: 3
- Required Packages: 
	- pandas
	- scipy
	- matplotlib
	- seaborn
	- pysurfer
	- nibabel
	- tableone

# Usage

## 01 - Image Processing
Goal: 
Original Usage: 

How to Use: 

## 02 - Analysis and Visualization
Goal: Analyze and visualize values output from Image Processing (i.e., CBF and ATT values from FreeSurfer ROIs)
Original Usage:
- Assumes data is organized within a folder structure including raw, intermediate, and processed sub-folders

How to Use: 
- In each file, change DATA_FOLDER to the location of the data folder
- [data folder]/raw should contain outputs from Image Processing
- File names are specific to the above project and will need to modified according to individual outputs

# Further Reading

## 01 - Image Processing
- https://fsl.fmrib.ox.ac.uk/fsl/docs/#/physiological/basil
- https://surfer.nmr.mgh.harvard.edu/fswiki/CorticalParcellation