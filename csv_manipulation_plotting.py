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
    #To set working directory:
    #os.chdir("/Filepath to CSV/")
    #Would be better to call this line using an optional function argument
    
    
    #Making a list of all CSV files (use BODY.csv to ensure other CSV's arent selected) in the given folder
    file_extension = 'BODY.csv'
    all_filenames = [i for i in glob.glob(f"*{file_extension}")]

    #Make a dataframe from the 1st file in the list just as a check 
    df = pd.read_csv(all_filenames[0], sep=',',delimiter=None)
    print ("\n---check info below---")
    print(df.shape)
    print(all_filenames[0])
    print (df.columns.values)
    print("----\n")
    
    #Loop through all files and concat to the dataframe
    df_combined_csv_data = pd.concat([pd.read_csv(f, sep=',', delimiter=None) for f in all_filenames])
    
    #If you need to save all the data to a CSV
    if create_csv == True:
        df_combined_csv_data.to_csv('combined_hk_gb_all_amnts_24_nov.csv')
        print ('\ncombined ',len(all_filenames),' into 1 CSV')
        
    return df_combined_csv_data



def select_provider(df, name_lst):
    #Creates a dataframe containing only info of the given provider (as per excel requirement)
    df_select_provider = df.loc[df['name'].isin(name_lst)]
    print (df_select_provider.shape)    
    return df_select_provider
    
    

    


def plotting (df, x_column, y_column, **kwargs):
    #Plot some x value against some y value for the provider chosen in by the function above

    #Sort values to for the line plot 
    df = df.sort_values(by=[x_column])
    plt.figure()
    
    #Plot (x_column, y_column) for the given dataframe
    #can use Kwargs to specifcy other plotting arguments e.g. color '#DB0011'for HSBC
    df.plot(x=x_column, y=y_column, marker='o', **kwargs)
    
    #Set axis labels and titles bassed on the function args
    #Could make this better by having some code which coverts a '_' to a space etc
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(df['name'].iloc[0])
    plt.show()
    return 





df = combine_all_csv()
name=['China Construction Bank']
df = select_provider(df,name)
plotting(df, 'send_amount', 'total_margin')

