
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




