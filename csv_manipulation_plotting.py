#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 14:04:15 2021

@author: callumzs
"""
import glob
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def combine_all_csv(create_csv = False):
    #To set working directory use:
    #os.chdir("/Filepath to CSV/")
    #Would be better to call this line using a Kwarg or boolean function argument
    
    
    #Making a list of all CSV files (use BODY.csv to ensure other CSV's arent selected) in the given folder
    file_extension = 'BODY.csv'
    all_filenames = [i for i in glob.glob(f"*{file_extension}")]

    #Make a dataframe from the 1st file in the list just as a check 
    df = pd.read_csv(all_filenames[0], sep=',',delimiter=None)
    print ("\n----Check Info Box----")
    print("df Shape: ", df.shape)
    print("0th Filename: ", all_filenames[0],)
    print ("\ndf Column Headers: ",  df.columns.values)
    print("-----------------------\n")
    
    #Loop through all files and concat to the dataframe
    df_combined_csv_data = pd.concat([pd.read_csv(f, sep=',', delimiter=None) for f in all_filenames])
    
    #If you need to save all the data to a CSV
    if create_csv == True:
        #Would be better to change the filename to a variable given by a Kwarg 
        df_combined_csv_data.to_csv('combined_hk_gb_all_amnts_24_nov.csv')
        print ('\ncombined ',len(all_filenames),' into 1 CSV')
        
    #Returns a pandas dataframe of the combined CSVs
    return df_combined_csv_data



def select_provider(df, name_lst):
    #Filters the dataframe to return a new dataframcontaining only the given providers (as per excel requirement)
    
    
    #Save the 'to currency' as a global variable - used for labeling graphs
    global df_to_currency 
    df_to_currency = df['to_currency'].iloc[4]
    
    
    #Doing the filtering
    df_select_provider = df.loc[df['name'].isin(name_lst)]
 
    #Return filtered dataframe
    return df_select_provider
    
    

    


def plotting (df, x_column, y_column, **kwargs):
    '''
    

    Parameters
    ----------
    df : Pandas Datafram
        The filtered dataframe (returned by select_provider function) which will 
        be used for plotting
    x_column : String
        The variable to be plotted on the x axis. Must be the exact CSV column header
        string (inc capitalisation)
    y_column : The variable to be plotted on the y axis. Must be the exact CSV column header
        string (inc capitalisation)
    **kwargs : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''

    provider = df['name']
    
    #Sort values for the line plot 
    df = df.sort_values(by=[x_column])
    
    
    np_data = df.to_numpy() #NOT USED
    print('plotting func: ')
    
    print (np.shape(np_data))
    plt.figure()
    
    #Number of rows in df np.shape(np_data)[0]
    
    #Below works for plotting multiple lines
    
    fig, ax = plt.subplots()

    
    #np.empty size=(np.shape((df)[some indexing], my choice) )

    for provider, group in df.groupby('name'):
    #Append average values to a multi-d array and return them
    #e.g. [[name 1, name 2, name 3],[mean 1, mean2, mean3],[std1, std2, std3]]    
        if 'HSBC' in provider:
            #If HSBC use HSBC color #DB0011
            group.plot(x=x_column, y=y_column, ax=ax, label=provider, marker ='o', color = '#DB0011')
        else:
            #else use defalut MatPlotLib color
            group.plot(x=x_column, y=y_column, ax=ax, label=provider, marker ='o')
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title('{} vs {} for HKD to {}'.format(y_column,x_column,df_to_currency))
    plt.show()
    
    
    '''
    Below works for plotting only 1 line 
    
    
    #Plot (x_column, y_column) for the given dataframe
    #can use Kwargs to specifcy other plotting arguments e.g. color '#DB0011'for HSBC
    df.plot(x=x_column, y=y_column, marker='o', **kwargs)
    
    #Set axis labels and titles bassed on the function args
    #Could make this better by having some code which coverts a '_' to a space etc
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(df['name'].iloc[0])
    plt.show()
    
    '''
    return 






df = combine_all_csv()
'China Construction Bank'
providers=['OFX','HSBC Hong Kong','China Construction Bank']

df = select_provider(df,providers)

plotting(df, 'send_amount', 'fx_margin')







    
    


