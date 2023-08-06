# Part of the 'explore' subpackage of 'larkinlab'
# functions for Exploratory Analysis
#
##################################################################################################################

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

##################################################################################################################

def dframe_ex(df):
    # create function to explore a dataframe's shape and size quickly
    
    # display shape and size
    print("Rows: ", df.shape[0])
    print("Columns: ", df.shape[1])
    print("Data Points: ", df.size, "\n")
    
    # print column names up to 100
    try:
        if df.shape[1] <= 60:
            print(df.columns)
        elif df.shape[1] > 60:
            print("First 60 columns: ", df.columns[:60])
                
    except Exception:
        try:
            print(df.columns)
        except Exception:
            raise #not sure if this is correct or not, would like it to return the error as normal if it doesn't work for debugging
         
    # display first 5 rows of df    
    return df.head()

##################################################################################################################

def vcount_ex(df):
    # a function to print the value counts and their corresponding percentages of all columns in a given dataframe.
    
    #creates bold font
    class font:
        bold = '\033[1m'
        end = '\033[0m'
    
    #creates temporary list of all columns in dataframe to iterate through
    dfcol_temp_list = []
    for column in df.columns:
        x = column
        dfcol_temp_list.append(df[x])
    
    #iterate through column list getting their value counts and normalized value counts, and print them out
    n = 0
    for col in dfcol_temp_list:
        temp_comp_val_count_var = pd.concat([col.value_counts(), col.value_counts(normalize=True).mul(100)], axis=1, keys=('counts', "percentage"))
        y = df.columns[n]    
        print(font.bold + y + font.end)
        print(temp_comp_val_count_var.head(), "\n\n")
        n = n + 1

##################################################################################################################

def scat_ex(df):
    # a function to return scatter plots of the value counts of all columns in a dataframe, for quick visual analysis of value counts
    for col in df.columns:
        
        #create temp dataframe to plot
        x = col
        scat_plot = df[x].value_counts()        
        scat_plot_df = pd.DataFrame(scat_plot)
        scat_plot_df = scat_plot_df.reset_index()
        scat_plot_df.columns = [x, 'val counts']
        
        #plot it
        plt.figure()
        plt.xlabel(x)
        plt.ylabel('val counts')
        plt.scatter(scat_plot_df.index.values, scat_plot_df['val counts'])

##################################################################################################################



##################################################################################################################



##################################################################################################################



##################################################################################################################



##################################################################################################################



##################################################################################################################



##################################################################################################################



##################################################################################################################



##################################################################################################################