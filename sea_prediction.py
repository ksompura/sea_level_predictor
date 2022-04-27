import numpy as np
import pandas as pd
from scipy import stats

# load data in 
url = "https://datahub.io/core/sea-level-rise/r/epa-sea-level.csv"

df = pd.read_csv(url)

df.head()
df.shape
df.info()
# appears that NOAA has a significant amount of Nulls so drop that column and only use CSIRO Adjusted Sea Level
df_clean = df.drop(axis=1, labels='NOAA Adjusted Sea Level')
df_clean.info()
#appears that there is data missing for one year, drop that year
