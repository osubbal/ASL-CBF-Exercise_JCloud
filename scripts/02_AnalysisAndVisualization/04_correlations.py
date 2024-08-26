# %% Notes

"""
- Pearsons R correlations are performed to assess the extent to which RPE and VO2max are associated with pre- to post-exercise differences in perfusion (ATT and CBF)

"""

# %% Import Packages
import pandas as pd
from scipy import stats

# %% Define constants

DATA_FOLDER = '/Path/to/project/data'

CBF_FILE = DATA_FOLDER + 'intermediate/240522_finaldataset_csf.csv'

ATT_FILE = DATA_FOLDER + 'intermediate/240522_finaldataset_att.csv'

OUT_FILE = DATA_FOLDER + 'processed/240522_ptests.csv'

# %% Define functions

def selectDifferenceMeasures(measures):
    differenceMeasures = []
    for measure in measures:
        if '.dif' in measure:
            differenceMeasures.append(measure)
    return differenceMeasures

def convertValidColsToFloat(dataframe):
    newDataframe = dataframe.copy()
    for column in list(dataframe.columns):
        try:
            newDataframe[column] = dataframe[column].astype(float)
        except:
            pass
    return newDataframe

# %% Compute t-tests

pScores = {
    'region' : [],
    'measurement' : [],
    'iV' : [],
    'pStatistic' : [],
    'pVal' : [],
    'pConfIntH' : [],
    'pConfIntL' : [],
    'pN' : []
}

for measurement in ['csf', 'att']:
    if measurement == 'csf':
        perfValues = pd.read_csv(CBF_FILE)
    elif measurement == 'att':
        perfValues = pd.read_csv(ATT_FILE)
    
    allRegionMeasures = list(perfValues.columns)
    allRegionDifferences = selectDifferenceMeasures(allRegionMeasures)
    
    for regionDifference in allRegionDifferences:
        for iV in ['rpe', 'vo2']:
            
            reducedPerfValues = perfValues.dropna(subset=[iV, regionDifference])
            iVValues = reducedPerfValues[iV]
            
            regionDifferenceValues = reducedPerfValues[regionDifference]
            
            pTest = stats.pearsonr(iVValues, regionDifferenceValues)
            cInt = pTest.confidence_interval()
        
            pScores['region'].append(regionDifference)
            pScores['measurement'].append(measurement)
            pScores['iV'].append(iV)
            pScores['pStatistic'].append(pTest.statistic)
            pScores['pVal'].append(pTest.pvalue)
            pScores['pN'].append(len(reducedPerfValues))
            
            pScores['pConfIntH'].append(cInt.high)
            pScores['pConfIntL'].append(cInt.low)
        
pScores = pd.DataFrame(pScores)
pScores = convertValidColsToFloat(pScores)
pScores.to_csv(OUT_FILE, index=False)
        
    
        
        
    