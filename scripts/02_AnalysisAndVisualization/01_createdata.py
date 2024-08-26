# %% Notes

"""
- CSF and ATT values for the left and right hippocampus are included in the CSF_FILE. These were not included in analyses because the input data could not be corrected for distortion, so subcortical/temporal ROIs may be subject to additional artifact. 
"""

# %% Import Packages
import pandas as pd

# %% Define constants

DATA_FOLDER = '/Path/to/project/data'

CBF_FILE = DATA_FOLDER + 'raw/2407_finalperfusionrois.csv'

ATT_FILE = DATA_FOLDER + 'raw/2407_finalattrois.csv'

DEMOS_FILE = DATA_FOLDER + 'raw/240522_finaldemos.csv'

OUT_FILE = DATA_FOLDER + 'intermediate/240522_finaldataset_{}.csv' #{} replaced with measurement type at time of saving

FREESURFER_LABELS = {
    '1002' : 'lh-caudalanteriorcingulate',
    '1011' : 'lh-lateraloccipital',
    '1012' : 'lh-lateralorbitofrontal',
    '1014' : 'lh-medialorbitofrontal',
    '1022' : 'lh-postcentral',
    '1023' : 'lh-posteriorcingulate',
    '1024' : 'lh-precentral',
    '1026' : 'lh-rostralanteriorcingulate',
    '1032' : 'lh-frontalpole',
    '1035' : 'lh-insula',
    '2002' : 'rh-caudalanteriorcingulate',
    '2011' : 'rh-lateraloccipital',
    '2012' : 'rh-lateralorbitofrontal',
    '2014' : 'rh-medialorbitofrontal',
    '2022' : 'rh-postcentral',
    '2023' : 'rh-posteriorcingulate',
    '2024' : 'rh-precentral',
    '2026' : 'rh-rostralanteriorcingulate',
    '2032' : 'rh-frontalpole',
    '2035' : 'rh-insula',
    '53' : 'lh-hippocampus', #included in CSF file, not in ATT or used in analyses
    '17' : 'rh-hippocampus' #included in CSF file, not in ATT or used in analyses
}

# %% Define functions

def convertFreesurferLabels(regions, map):
    relabeledRegions = regions[:]
    for index, region in enumerate(regions):
        relabeledRegions[index] = map[region]
    return relabeledRegions

def calculatePrePostDifference(dataframe, map):
    newDataframe = dataframe.copy()
    labelsInDataframe = list(dataframe.columns)
    for region in map:
        preLabel = map[region] + '.1'
        postLabel = map[region] + '.2'
        differenceLabel = map[region] + '.dif'
        
        if preLabel in labelsInDataframe and postLabel in labelsInDataframe:
            newDataframe[differenceLabel] = dataframe[postLabel] - dataframe[preLabel]
    return newDataframe

# %% Clean CSF and ATT values dataframe 

for measurement in ['csf', 'att']:
    if measurement == 'csf':
        perfValues = pd.read_csv(CBF_FILE)
    elif measurement == 'att':
        perfValues = pd.read_csv(ATT_FILE)
        
    perfValues['region'] = perfValues['region'].astype(str)
    perfValues['run'] = perfValues['run'].astype(str)

    allRegions = list(perfValues['region'])
    perfValues['region'] = convertFreesurferLabels(allRegions, FREESURFER_LABELS)

    perfValues = pd.pivot(perfValues, index='ID', columns=['region', 'run'], values='meanPerfusion')

    perfValues.columns = ['.'.join(region) for region in perfValues.columns.values]

    perfValues = calculatePrePostDifference(perfValues, FREESURFER_LABELS)
    
    demoValues = pd.read_csv(DEMOS_FILE, index_col='ID')
    
    combinedValues = pd.concat([perfValues, demoValues], axis=1)
    
    measurementOutFile = OUT_FILE.format(measurement)
    combinedValues.to_csv(measurementOutFile)

