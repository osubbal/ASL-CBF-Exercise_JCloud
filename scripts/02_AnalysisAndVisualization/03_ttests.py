# %% Notes

"""
- T-tests assessing whether pre- and post-exercise perfusion values differ significantly are calculated as 1-sample t-tests on the difference between the two groups (equivalent mathematically to paired sample t-test)

"""

# %% Import Packages
import pandas as pd
from scipy import stats

# %% Define constants

DATA_FOLDER = '/Path/to/project/data'

CBF_FILE = DATA_FOLDER + 'intermediate/240522_finaldataset_csf.csv'

ATT_FILE = DATA_FOLDER + 'intermediate/240522_finaldataset_att.csv'

OUT_FILE = DATA_FOLDER + 'processed/240522_ttests.csv'

NULL_HYPOTHESIS = 0 #testing if pre- and post- perfusion differences are different from zero

# %% Define functions

def selectDifferenceMeasures(measures):
    differenceMeasures = []
    for measure in measures:
        if '.dif' in measure:
            differenceMeasures.append(measure)
    return differenceMeasures

# %% Compute t-tests

tScores = {
    'region' : [],
    'measurement' : [],
    'tStatistic' : [],
    'tPVal' : [],
    'tDF' : []
}

for measurement in ['csf', 'att']:
    if measurement == 'csf':
        perfValues = pd.read_csv(CBF_FILE)
    elif measurement == 'att':
        perfValues = pd.read_csv(ATT_FILE)
    
    allRegionMeasures = list(perfValues.columns)
    allRegionDifferences = selectDifferenceMeasures(allRegionMeasures)
    
    for regionDifference in allRegionDifferences:
        regionDifferenceValues = perfValues[regionDifference]
        tTest = stats.ttest_1samp(regionDifferenceValues, NULL_HYPOTHESIS)
        
        tScores['region'].append(regionDifference)
        tScores['measurement'].append(measurement)
        tScores['tStatistic'].append(tTest.statistic)
        tScores['tPVal'].append(tTest.pvalue)
        tScores['tDF'].append(tTest.df)
        
tScores = pd.DataFrame(tScores)
tScores.to_csv(OUT_FILE, index=False)
        
    
        
        
    