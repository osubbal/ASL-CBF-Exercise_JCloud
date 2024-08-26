# %% Notes

"""
- If this script is run via most GUIs (VSCode, Jupyter), the kernel will crash upon completion. All files will be exported correctly. 
"""

# %% Import packages

import os
import numpy as np
import nibabel as nib
from surfer import Brain
import pandas as pd

# %% Define constants

DATA_FOLDER = '/Path/to/project/data'

TSCORE_FILE = DATA_FOLDER + 'processed/240522_ttests.csv'

CORR_FILE = DATA_FOLDER + 'processed/240522_ptests.csv'

OUT_FILE_PREFIX = DATA_FOLDER + 'processed/'

SURFACE_SUBJECT = 'fsaverage'
SURFACE_SHAPE = 'inflated'
FREESURFER_DIRECTORY = '/Applications/freesurfer/7.1.1/subjects'
APARC_FILE = os.path.join(FREESURFER_DIRECTORY, SURFACE_SUBJECT, 'label', '{}.aparc.annot')

INCLUSION_THRESHOLD = 0.1 #p-value threshold for inclusion in figures
NULL_VALUE = 0 #value to plot if the region is not included in figure
PLOTTING_TRANSPARENCY = 0.8
P_PLOTTING_RANGE = 1 #absolute scale to plot correlations on
T_PLOTTING_RANGE = 3 #absolute scale to plot TScores on

# %% Define functions

# %% Generate brains

tScoreValues = pd.read_csv(TSCORE_FILE)
pValues = pd.read_csv(CORR_FILE)

for test in ['pTest', 'tTest']:
    if test == 'pTest':
        testValues = pValues.copy()
        statLabel = 'pStatistic'
        pLabel = 'pVal'
    elif test == 'tTest':
        testValues = tScoreValues.copy()
        statLabel = 'tStatistic'
        pLabel = 'tPVal'
        
    for measurement in ['csf', 'att']:
        for iV in ['rpe', 'vo2']:
            if test == 'pTest':
                measurementValues = testValues[testValues['measurement'] == measurement]
                measurementValues = measurementValues[measurementValues['iV'] == iV]
            elif test == 'tTest':
                measurementValues = testValues[testValues['measurement'] == measurement]
                iV = 'x'
                
            allAnalyzedRegions = list(measurementValues['region'])
            measurementValues = measurementValues.set_index('region')
        
            for hemisphere in ['lh', 'rh']:
            
                scoresByRegion = []
                
                freesurferLabels, freesurferCTab, freesurferRegions = nib.freesurfer.read_annot(APARC_FILE.format(hemisphere))
                
                for region in freesurferRegions:
                    regionIncluded = False
                    freesurferRegionLabel = '{}-{}.dif'.format(hemisphere, region.decode('UTF-8'))
                    
                    if freesurferRegionLabel in allAnalyzedRegions:
                        statScore = measurementValues.at[freesurferRegionLabel, statLabel]
                        pVal = measurementValues.at[freesurferRegionLabel, pLabel]
                        
                        if pVal <= INCLUSION_THRESHOLD:
                            scoresByRegion.append(statScore)
                            regionIncluded = True
                            
                    if not regionIncluded:
                        scoresByRegion.append(NULL_VALUE)
                        
                scoresByRegion = np.array(scoresByRegion) #format for PySurfer plotting
                regionsToPlotByVertex = scoresByRegion[freesurferLabels] 
                
                brain = Brain(SURFACE_SUBJECT, hemisphere, SURFACE_SHAPE, background='white', subjects_dir=FREESURFER_DIRECTORY)
                
                if test == 'pTest':
                    brain.add_data(regionsToPlotByVertex, min=-P_PLOTTING_RANGE, max=P_PLOTTING_RANGE, colormap='seismic', alpha=PLOTTING_TRANSPARENCY)
                elif test == 'tTest':
                    brain.add_data(regionsToPlotByVertex, min=-T_PLOTTING_RANGE, max=T_PLOTTING_RANGE, colormap='seismic', alpha=PLOTTING_TRANSPARENCY)
                
                brain.show_view('lateral')
                brain.save_image(OUT_FILE_PREFIX + test + '_' + iV + '_' + hemisphere + '_' + measurement + '_lat.png')
                
                if hemisphere == 'lh':
                    brain.show_view({'azimuth': 40, 'elevation': 90}, roll=-90)
                elif hemisphere == 'rh':
                    brain.show_view({'azimuth': -40, 'elevation': -90}, roll=90)
                    
                brain.save_image(OUT_FILE_PREFIX + test + '_' + iV + '_' + hemisphere + '_' + measurement + '_med.png')
