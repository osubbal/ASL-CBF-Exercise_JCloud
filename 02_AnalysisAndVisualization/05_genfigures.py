# %% Import packages

import pandas as pd
import seaborn as sns
import matplotlib
from matplotlib import rcParams
import matplotlib.pyplot as plt

# %% Set constants

DATA_FOLDER = '/Path/to/project/data'
SRC_FOLDER = '/Path/to/project/src'

CBF_FILE = DATA_FOLDER + 'intermediate/240522_finaldataset_csf.csv'

# %% Define functions

# %% Set figure aesthetics
cmap = sns.diverging_palette(230, 20, as_cmap=True)
matplotlib.style.use(DATA_FOLDER + 'apa.mplstyle')
sns.set(font='Arial', style="ticks")
rcParams['figure.figsize'] = 6,6

# %% Generate boxplot

cbf_values = pd.read_csv(CBF_FILE)

# reshape wide dataframe to long for easier plotting, including only regions we want to plot
cbf_values_long = cbf_values.melt(id_vars='ID', value_vars=['lh-insula.1', 'lh-insula.2', 'lh-rostralanteriorcingulate.1', 'lh-rostralanteriorcingulate.2'])
cbf_values_long = cbf_values_long.join(cbf_values_long['variable'].str.split('.', n=1, expand=True).rename(columns={0:'region', 1:'timepoint'}))

cbf_values_long['region'] = pd.Categorical(cbf_values_long['region'])
cbf_values_long['timepoint'] = pd.Categorical(cbf_values_long['timepoint'])
cbf_values_long['region'] = cbf_values_long['region'].cat.rename_categories({'lh-insula' : 'Insula', 'lh-rostralanteriorcingulate' : 'Rostral Anterior Cingulate'})
cbf_values_long['timepoint'] = cbf_values_long['timepoint'].cat.rename_categories({'1' : 'Pre-Exercise', '2' : 'Post-Exercise'})

ax = sns.boxplot(data=cbf_values_long, x="region", y="value", hue='timepoint', palette = "mako", width=.5)
ax.set_xlabel('Time Point')
ax.set_ylabel('Insular Cortex, Left Hemisphere')
plt.savefig(DATA_FOLDER + 'processed/tTest_boxplots.png', dpi=300)

# %% General scatter plot

# reshape wide dataframe to long for easier plotting, including only regions we want to plot
cbf_values_long = cbf_values.melt(id_vars=['ID', 'rpe'], value_vars=['rh-insula.dif', 'rh-medialorbitofrontal.dif'])

cbf_values_long['variable'] = pd.Categorical(cbf_values_long['variable'])
cbf_values_long['variable'] = cbf_values_long['variable'].cat.rename_categories({'rh-insula.dif' : 'Insula', 'rh-medialorbitofrontal.dif' : 'Medial Orbitofrontal Cortex'})

ax = sns.lmplot(data=cbf_values_long, x="value", y="rpe", col='variable', palette = "mako")
ax.set_axis_labels('Post-Exercise Difference in Cerebral Blood Flow', 'Ratings of Perceived Exertion', )
plt.savefig(DATA_FOLDER + 'processed/pTest_correlations.png', dpi=300)

