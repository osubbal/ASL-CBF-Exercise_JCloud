# %% Notes

"""

"""

# %% Import Packages
import pandas as pd
from tableone import TableOne

# %% Define constants

DATA_FOLDER = '/Path/to/project/data'

DEMOS_FILE = DATA_FOLDER + 'raw/240522_finaldemos.csv'

OUT_FILE = DATA_FOLDER + 'processed/240522_tableone.csv'

INCLUDE_COLUMNS = ['rpe', 'vo2', 'age', 'sex', 'education', 'race', 'gen_health_rating', 'weight', 'height', 'days_activity', 'moca_score']

CATEGORICAL_COLUMNS = ['sex', 'race', 'gen_health_rating']

# %% Define functions

# %% Compute demographics

demoValues = pd.read_csv(DEMOS_FILE)

demoTable = TableOne(demoValues, INCLUDE_COLUMNS, CATEGORICAL_COLUMNS)

demoTable.to_csv(OUT_FILE)

