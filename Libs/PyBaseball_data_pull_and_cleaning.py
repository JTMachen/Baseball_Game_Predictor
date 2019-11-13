# Import necessary libraries
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pybaseball import batting_stats_range, pitching_stats_range

def get_batting_data(start_date, end_date):
    """ Takes a start and end date and will return a dataframe of daily hitting statistics for every player
        that played for each day in the date range. start_date and end_date should be in YYYY-MM-DD format.  Data is 
        being pulled from the PyBaseball API using their batting_stats_range() function. Each iteration through the date 
        range will print out the current date or if no games were played that day.
    """
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    dates_generator = [start + timedelta(days=x) for x in range(0, ((end-start).days) + 1)]
    dates = [date.strftime("%Y-%m-%d") for date in dates_generator]
    batting_data_df = pd.DataFrame()
    batting_data = pd.DataFrame()
    for date in dates:
        try:
            batting_data = batting_stats_range(date) 
            batting_data_df = batting_data_df.append(batting_data) 
            print(date)
        except:
            print('Game not played')

    return batting_data_df


def clean_batting_data(df):
    """ Takes a dataframe pulled from the PyBaseball API using the get_batting_data() function located in this
        library.  Will return a dataframe that has dropped unneeded columns and cleaned up other columns for
        feature selection in a machine learning program. The columns on years before 2017 have different names
        and this function will not work for them.  There is not consistency in the dataframes before 2017.
    """
    df.drop(columns = ['Age','#days', 'BA', 'OBP', 'SLG', 'OPS'], inplace = True)
    df = df.rename(columns = {'\xa0': 'VH'})  
    df['VH'] = df['VH'].replace('@',1)
    df['VH'] = df['VH'].replace('', 0) 
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')
    return df

def get_pitching_data(start_date, end_date):
    """ Takes a start and end date and will return a dataframe of daily pitching statistics for every player
        that played for each day in the date range. start_date and end_date should be in YYYY-MM-DD format.  Data is 
        being pulled from the PyBaseball API using their pitching_stats_range() function. Each iteration through the date 
        range will print out the current date or if no games were played that day.
    """
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    dates_generator = [start + timedelta(days=x) for x in range(0, ((end-start).days) + 1)]
    dates = [date.strftime("%Y-%m-%d") for date in dates_generator]
    pitching_data_df = pd.DataFrame()
    pitching_data = pd.DataFrame()
    for date in dates:
        try:
            pitching_data = pitching_stats_range(date) 
            pitching_data_df = pitching_data_df.append(pitching_data) 
            print(date)
        except:
            print('Game not played')

    return pitching_data_df

def clean_pitching_data(df):
    """ Takes a dataframe pulled from the PyBaseball API using the get_pitching_data() function located in this
        library.  Will return a dataframe that has dropped unneeded columns and cleaned up other columns for
        feature selection in a machine learning program. The columns on years before 2018 have different names
        and this function will not work for them.  There is not consistency in the dataframes before 2018.
    """
    df.drop(columns = ['Age','#days', 'W', 'L', 'SV', 'GSc'], inplace = True)
    df = df.rename(columns = {'\xa0': 'VH'})  
    df['VH'] = df['VH'].replace('@',1)
    df['VH'] = df['VH'].replace('', 0) 
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')
    return df