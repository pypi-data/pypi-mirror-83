"""My chocobo cooking script."""
"""I left the chocobo here because I want to thank the chocobo package
""author for teaching me how to package!"""
import os
import warnings
import scipy
from sklearn.preprocessing import StandardScaler
import scipy.stats
from statsmodels.distributions.empirical_distribution import ECDF
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

def last_period (df,interval,periods,date_column,to_past,unique_id='NULL'):
    """df: the dataframe"""
    """interval: hours, days or weeks"""
    """periods: #of interval"""
    """to_past: list"""
    """unique_id: (optional) list"""
    
    import warnings
    warnings.filterwarnings("ignore")
    
    def concatenate_list_data(list):
        result= ''
        for element in list:
            result += str(element)
        return result
        
    
    df['num'] = df.index
    
    prefix = 'l'+str(periods)+interval[0]
    
    if interval == 'weeks':
         df[prefix] = df[date_column].apply(lambda x: x- timedelta(weeks=periods))
    if interval == 'days':
         df[prefix] = df[date_column].apply(lambda x: x- timedelta(days=periods))
    if interval == 'hours':
         df[prefix] = df[date_column].apply(lambda x: x- timedelta(days=periods))
    
    
    
    
    if unique_id == 'NULL':
        for col in to_past:
            col_name = 'v'+col
            df[col_name] = df['num'].apply(lambda x: df[col][x]/    
                                df[(df[date_column]==df[prefix][x])][col].sum())        
    else:
        if len(unique_id)==1:
            for col in to_past:
                col_name = 'v'+col
                df[col_name] = df['num'].apply(lambda x: df[col][x]/    
                                    df[(df[unique_id[0]]==df[unique_id[0]][x]) & (df[date_column]==df[prefix][x])][col].sum())
                                             
        else:
            df_clean = df[unique_id]
            df['primarykey'] = df_clean.sum(axis=1).astype(str)
            for col in to_past:
                col_name = 'v'+col
                df[col_name] = df['num'].apply(lambda x: df[col][x]/    
                                    df[(df['primarykey']==df['primarykey'][x]) & (df[date_column]==df[prefix][x])][col].sum())
                
    df = df[~df.isin([np.nan, np.inf, -np.inf]).any(1)]
    return df