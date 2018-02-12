
# coding: utf-8

# # Assignment 4
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# This assignment requires that you to find **at least** two datasets on the web which are related, and that you visualize these datasets to answer a question with the broad topic of **economic activity or measures** (see below) for the region of **Ann Arbor, Michigan, United States**, or **United States** more broadly.
# 
# You can merge these datasets with data from different regions if you like! For instance, you might want to compare **Ann Arbor, Michigan, United States** to Ann Arbor, USA. In that case at least one source file must be about **Ann Arbor, Michigan, United States**.
# 
# You are welcome to choose datasets at your discretion, but keep in mind **they will be shared with your peers**, so choose appropriate datasets. Sensitive, confidential, illicit, and proprietary materials are not good choices for datasets for this assignment. You are welcome to upload datasets of your own as well, and link to them using a third party repository such as github, bitbucket, pastebin, etc. Please be aware of the Coursera terms of service with respect to intellectual property.
# 
# Also, you are welcome to preserve data in its original language, but for the purposes of grading you should provide english translations. You are welcome to provide multiple visuals in different languages if you would like!
# 
# As this assignment is for the whole course, you must incorporate principles discussed in the first week, such as having as high data-ink ratio (Tufte) and aligning with Cairo’s principles of truth, beauty, function, and insight.
# 
# Here are the assignment instructions:
# 
#  * State the region and the domain category that your data sets are about (e.g., **Ann Arbor, Michigan, United States** and **economic activity or measures**).
#  * You must state a question about the domain category and region that you identified as being interesting.
#  * You must provide at least two links to available datasets. These could be links to files such as CSV or Excel files, or links to websites which might have data in tabular form, such as Wikipedia pages.
#  * You must upload an image which addresses the research question you stated. In addition to addressing the question, this visual should follow Cairo's principles of truthfulness, functionality, beauty, and insightfulness.
#  * You must contribute a short (1-2 paragraph) written justification of how your visualization addresses your stated research question.
# 
# What do we mean by **economic activity or measures**?  For this category you might look at the inputs or outputs to the given economy, or major changes in the economy compared to other regions.
# 
# ## Tips
# * Wikipedia is an excellent source of data, and I strongly encourage you to explore it for new data sources.
# * Many governments run open data initiatives at the city, region, and country levels, and these are wonderful resources for localized data sources.
# * Several international agencies, such as the [United Nations](http://data.un.org/), the [World Bank](http://data.worldbank.org/), the [Global Open Data Index](http://index.okfn.org/place/) are other great places to look for data.
# * This assignment requires you to convert and clean datafiles. Check out the discussion forums for tips on how to do this from various sources, and share your successes with your fellow students!
# 
# ## Example
# Looking for an example? Here's what our course assistant put together for the **Ann Arbor, MI, USA** area using **sports and athletics** as the topic. [Example Solution File](./readonly/Assignment4_example.pdf)

# In[4]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
    
def get_data(dataFile):
    
    df10 = pd.read_csv(dataFile)
    
    try:
        df10['Unemployment (Some College)'] = df10['HC04_EST_VC41']
        df10['Unemployment (no College)'] = df10['HC04_EST_VC40']
    except KeyError:
        try:
            df10['Unemployment (Some College)'] = df10['HC04_EST_VC46']
            df10['Unemployment (no College)'] = df10['HC04_EST_VC45']
        except KeyError:
            try:
                df10['Unemployment (Some College)'] = df10['HC04_EST_VC40']
                df10['Unemployment (no College)'] = df10['HC04_EST_VC39']
            except KeyError:
                df10['Unemployment (Some College)'] = df10['HC04_EST_VC34']
                df10['Unemployment (no College)'] = df10['HC04_EST_VC33']
            
    
    df10 = df10.drop(df10.columns[:-2], axis=1).drop(0)
    
    return df10

def get_unemployment():
    df = pd.read_excel('Unemployment_data.xlsx', skiprows=10)
    df = df.set_index('Year')
    df = df.drop([2007, 2008])
    df = df.mean(axis=1)
    
    return df

def build_dataFrame():
    
    index = [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016]
    dataFiles = ['09_5YR.csv', '10_5YR.csv', '11_5YR.csv', '12_5YR.csv', '13_5YR.csv', '14_5YR.csv', '15_5YR.csv', '16_5YR.csv']

    dfList = [get_data(x) for x in dataFiles]

    df = dfList[0]
    df.loc[2009] = df.loc[1]
    df.loc[2010] = dfList[1].loc[1]
    df.loc[2011] = dfList[2].loc[1]
    df.loc[2012] = dfList[3].loc[1]
    df.loc[2013] = dfList[4].loc[1]
    df.loc[2014] = dfList[5].loc[1]
    df.loc[2015] = dfList[6].loc[1]
    df.loc[2016] = dfList[7].loc[1]
    df = df.reindex(index)

    df['Gen. Ann Arbor Unemployment'] = get_unemployment()

    return df

def build_chart():
    plt.figure()
    ax = plt.subplot(1,1,1)
    df = build_dataFrame()
    
    for column in df.columns:
        ax.plot(df[column], label=str(column))
        
    #ax.plot(df[df.columns[0]], label=str(df.columns[0]))
    #ax.plot(df)
    ax.legend()
    ax.set_title('Unemployment and Education for 2009-2016 in Ann Arbor, MI')
    ax.set_ylabel('Percent Unemployed')
    ax.get_figure().savefig('unemployment_chart.png')
    
    plt.show()
    

build_chart()


# In[2]:


###########################################################################################################################
## How the 2008 recession effected the employment of high school grads vs those with some college exp. in Ann Arbour, MI ##
###########################################################################################################################


# In[ ]:



