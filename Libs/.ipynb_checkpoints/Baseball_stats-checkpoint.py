def baseball_stats_calculator_hitting(df) : 
    '''This function will calculate hitting statistics over the look back period of the batting_df.  It will return a df with columns added for K%, BB%, OBP, and SLG% ''' 
    
    home_and_visitor = ['Home_Hitting', 'Visitor_Hitting']
    
    for i in range(2):
        df[home_and_visitor[i] + 'K%'] = df[home_and_visitor[i] + 'SO'] / df[home_and_visitor[i] + 'PA']
        df[home_and_visitor[i] + 'BB%'] = df[home_and_visitor[i] + 'BB'] / df[home_and_visitor[i] + 'PA']
        df[home_and_visitor[i] + 'OBP_num'] = df[home_and_visitor[i] + 'H'] + df[home_and_visitor[i] + 'BB']+ df[home_and_visitor[i] + 'HBP']                                   
        df[home_and_visitor[i] + 'OBP_den'] = df[home_and_visitor[i] + 'AB'] + df[home_and_visitor[i] + 'BB'] + df[home_and_visitor[i] + 'HBP'] + df[home_and_visitor[i] + 'SF']
        df[home_and_visitor[i] + 'OBP'] = df[home_and_visitor[i] + 'OBP_num'] / df[home_and_visitor[i] + 'OBP_den']
        df[home_and_visitor[i] + '1B'] = df[home_and_visitor[i] + 'H'] - (df[home_and_visitor[i] + '2B'] + df[home_and_visitor[i] + '3B'] + df[home_and_visitor[i] + 'HR'])
        df[home_and_visitor[i] + 'SLG%_num'] = df[home_and_visitor[i] + '1B'] + 2 * df[home_and_visitor[i] + '2B'] + 3 * df[home_and_visitor[i] + '3B'] + 4 * df[home_and_visitor[i] + 'HR']
        df[home_and_visitor[i] + 'SLG%_den'] = df[home_and_visitor[i] + 'AB']
        df[home_and_visitor[i] + 'SLG%'] = df[home_and_visitor[i] + 'SLG%_num'] / df[home_and_visitor[i] + 'SLG%_den']
    return df


def baseball_stats_calculator_pitching(df) : 
    ''' This function will calculate hitting statistics over the look back period of the batting_df.  It will return a df with columns added for K%, BB%, OBP, and SLG% '''
    
    home_and_visitor = ['Home_Pitching', 'Visitor_Pitching']

    for i in range(2):
        df[home_and_visitor[i] + 'K%'] = df[home_and_visitor[i] + 'SO'] / df[home_and_visitor[i] + 'BF']
        df[home_and_visitor[i] + 'BB%'] = df[home_and_visitor[i] + 'BB'] / df[home_and_visitor[i] + 'BF']
        df[home_and_visitor[i] + 'OBP_num'] = df[home_and_visitor[i] + 'H'] + df[home_and_visitor[i] + 'BB']+ df[home_and_visitor[i] + 'HBP']                                   
        df[home_and_visitor[i] + 'OBP_den'] = df[home_and_visitor[i] + 'AB'] + df[home_and_visitor[i] + 'BB'] + df[home_and_visitor[i] + 'HBP'] + df[home_and_visitor[i] + 'SF']
        df[home_and_visitor[i] + 'OBP_allowed'] = df[home_and_visitor[i] + 'OBP_num'] / df[home_and_visitor[i] + 'OBP_den']
        df[home_and_visitor[i] + '1B'] = df[home_and_visitor[i] + 'H'] - (df[home_and_visitor[i] + '2B'] + df[home_and_visitor[i] + '3B'] + df[home_and_visitor[i] + 'HR'])
        df[home_and_visitor[i] + 'SLG%_num'] = df[home_and_visitor[i] + '1B'] + 2 * df[home_and_visitor[i] + '2B'] + 3 * df[home_and_visitor[i] + '3B'] + 4 * df[home_and_visitor[i] + 'HR']
        df[home_and_visitor[i] + 'SLG%_den'] = df[home_and_visitor[i] + 'AB']
        df[home_and_visitor[i] + 'SLG%_allowed'] = df[home_and_visitor[i] + 'SLG%_num'] / df[home_and_visitor[i] + 'SLG%_den']
    return df