
# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **Ann Arbor, Michigan, United States**, and the stations the data comes from are shown on the map below.

import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd
import numpy as np

df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')
#######################################################################
### Remove Leap Year Days (feb day = 29) ################################
df['Date'] = pd.to_datetime(df['Date'])

df15 = df.copy()

df['Date'] = df['Date'].apply(lambda x: None if (x.month == 2 and x.day == 29) or (x.year > 2014) else x)

df = df.dropna().set_index('Date').sort_index()

########################################################
### Separate Highs from Lows #############################
names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']

groups = df.groupby(by=[df.index.month, df.index.day, df['Element']])

HighTemps = groups.agg(np.max)
LowTemps = groups.agg(np.min)

HighTemps.index.set_levels(names, inplace=True, level=0)
LowTemps.index.set_levels(names, inplace=True, level=0)

High = HighTemps.xs('TMAX', level=2)
Low = LowTemps.xs('TMIN', level=2)

########################################################
#### Handle 2015 Data ##################################
df15['Date'] = df15['Date'].apply(lambda x: None if x.year != 2015 else x)
df15 = df15.dropna().set_index('Date').sort_index()

groups15 = df15.groupby(by=[df15.index.month, df15.index.day, df15['Element']])

HighTemps15 = groups15.agg(np.max)
LowTemps15 = groups15.agg(np.min)

HighTemps15.index.set_levels(names, inplace=True, level=0)
LowTemps15.index.set_levels(names, inplace=True, level=0)

High15 = HighTemps15.xs('TMAX', level=2)
Low15 = LowTemps15.xs('TMIN', level=2)

Low15['High'] = High15['Data_Value']/10 # Low15 becomes holder of both High and Low values
Low15['Low'] = Low15['Data_Value']/10
Low15 = Low15.drop(['Data_Value'], axis=1).reset_index()
Low15.columns = ['Month', 'Day', 'ID', 'High', 'Low']

values15H = pd.Series()
values15L = pd.Series()

###################################################
### Plot ##########################################

Temps = pd.DataFrame()
Temps = High
Temps['High'] = Temps['Data_Value']/10
Temps['Low'] = Low['Data_Value']/10
Temps = Temps.drop(['Data_Value'], axis=1)

Temps = Temps.reset_index()
Temps.columns = ['Month', 'Day', 'ID', 'High', 'Low']

#####################

values15H = Low15[Temps['High'] < Low15['High']]['High']
values15L = Low15[Temps['Low'] > Low15['Low']]['Low']


##########################

###################################

xVals = [x for x in range(0,365,31)]

###################################

fig, sub = plt.subplots()
ax = Temps['Low'].plot(alpha=.65, label='Low')
Temps['High'].plot(x = 'a', y='b', xticks = xVals, ax = ax, color='red', alpha=.65, label="High")
ax.set_xticklabels(names)
ax.fill_between(Temps.index, Temps['High'], Temps['Low'], facecolor='orange', alpha=.1)
ax.set_xlabel('Month')
ax.set_ylabel('Temperature in Degrees Celsius')
ax.scatter(x=values15H.index, y=values15H.values, color = 'black', label="2015 High")
ax.scatter(x=values15L.index, y=values15L.values, color='purple', label='2015 Low')

ax.set_title('Temperature Highs and Lows from 2005-2014 with 2015 Extremes')


ax.legend()
ax.get_figure().savefig('chart.png')


plt.show()




