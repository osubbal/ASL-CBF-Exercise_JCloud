# %% Notes

"""
- T-tests assessing whether pre- and post-exercise perfusion values differ significantly are calculated as 1-sample t-tests on the difference between the two groups (equivalent mathematically to paired sample t-test)

"""

# %% Import Packages
import pandas as pd
from scipy import stats

# %% Define constants

DATA_FOLDER = '/Path/to/project/data'

FD_FILE = DATA_FOLDER + 'raw/240604_asl_qc.csv'

OUT_FILE = DATA_FOLDER + 'processed/240604_qc_ttests.csv'

NULL_HYPOTHESIS = 0 #testing if pre- and post- perfusion differences are different from zero

# %% Define functions

# %% Reorient data

fdValues = pd.read_csv(FD_FILE)

fdValues['run'] = fdValues['run'].astype(str)

fdValues = pd.pivot(fdValues, index='sub', columns='run', values=['medfd', 'meanfd'])
fdValues.columns = ['.'.join(fd) for fd in fdValues.columns.values]

fdValues['medfd.dif'] = fdValues['medfd.2'] - fdValues['medfd.1']
fdValues['meanfd.dif'] = fdValues['meanfd.2'] - fdValues['meanfd.1']

# %% Compute t-tests

tScores = {
    'measurement' : [],
    'tStatistic' : [],
    'tPVal' : [],
    'tDF' : []
}

for measurement in ['mean', 'med']:

    fdDifferenceValues = fdValues[measurement + 'fd.dif']
    tTest = stats.ttest_1samp(fdDifferenceValues, NULL_HYPOTHESIS)

    tScores['measurement'].append(measurement)
    tScores['tStatistic'].append(tTest.statistic)
    tScores['tPVal'].append(tTest.pvalue)
    tScores['tDF'].append(tTest.df)
            
tScores = pd.DataFrame(tScores)
tScores.to_csv(OUT_FILE, index=False)