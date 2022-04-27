from turtle import color
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# load data in 
url = "https://datahub.io/core/sea-level-rise/r/epa-sea-level.csv"

# parse dates, set year as index
df = pd.read_csv(url, parse_dates=True)

df.head()
df.shape
df.info()

# appears that NOAA has a significant amount of Nulls so drop that column and only use CSIRO Adjusted Sea Level
df_clean = df.drop(axis=1, labels='NOAA Adjusted Sea Level')
df_clean.info()

#appears that there is data missing for one year, drop that year
df_clean = df_clean.dropna()
df_clean.info()

# Year is an object type, make it into datetime - try parse_dates=True when reading in
print(df_clean)

# Make year column only the year, not the day and month because they all appear to be on March 15th
df_clean['year'] = pd.DatetimeIndex(df_clean['Year']).year
df_clean = df_clean.drop(axis=1, labels='Year')

# grouby year to check if there are any duplicate years
df_clean.groupby(df_clean["year"])["year"].count()
df_clean.year.value_counts()

# there are no duplicate years so set years as index
df = df_clean.set_index('year')



# create scatter plot with year and sea level
sns.set_theme(style = 'whitegrid')
sns.scatterplot(data=df, x='year', y='CSIRO Adjusted Sea Level')
plt.xlabel('Year')
plt.ylabel('Sea Level (inches)')
plt.title('Rise in Sea Level since 1880')
plt.show()

# use a linear regression to get slope and y-intercept and plot the line of best fit over the plot
# need to create x and y array like variables to for the linear regression model

# set X as years
X = df.index.to_numpy()

# set Y as sea level
Y = df['CSIRO Adjusted Sea Level'].to_numpy()

# create linear regression model
linreg = stats.linregress(X,Y)


# create plot with linear regresion line
sns.scatterplot(data=df, x='year', y='CSIRO Adjusted Sea Level')
plt.plot(X, X*linreg.slope + linreg.intercept, color='orange')
plt.xlabel('Year')
plt.ylabel('Sea Level (inches)')
plt.title('Rise in Sea Level since 1880')
plt.show()

# extend regression line out to the year 2050
future_year = np.arange(1880, 2051)
sns.scatterplot(data=df, x='year', y='CSIRO Adjusted Sea Level')
plt.plot(future_year, future_year*linreg.slope + linreg.intercept, color='orange')
plt.xlabel('Year')
plt.ylabel('Sea Level (inches)')
plt.title('Rise in Sea Level since 1880')
plt.show()

# create a new regression model begining from the year 2000 to 2013 (most recent year) in order to see recent sea level changes
X_2000 = np.extract(X >= 2000, X)
X_2000

# extract the last 14 element of Y to match to the years 2000 to 2013
Y_2000 = Y[-14:]

lin_2000 = stats.linregress(X_2000, Y_2000)

recent_year = np.arange(2000,2051)

# add new regression line in the year 2000


sns.scatterplot(data=df, x='year', y='CSIRO Adjusted Sea Level')
sns.lineplot(recent_year, recent_year*lin_2000.slope + lin_2000.intercept, color='red', label='Rise: 0.17 in/year')
sns.lineplot(future_year, future_year*linreg.slope + linreg.intercept, color='orange', label='Rise: 0.06 in/year',linestyle='dashed')
plt.legend()
plt.xlabel('Year')
plt.ylabel('Sea Level (inches)')
plt.suptitle('Rise in Sea Level since 1880')
plt.title('Data Source: US Environmental Protection Agency',loc='right',fontdict = {'fontsize' : 7})
plt.show()

