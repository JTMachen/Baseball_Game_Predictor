import pandas as pd


# Define function for cleaning dataframe
def clean_lineups(df):
    """Removes the posistions from each of the lineups dataframes in order to better combine with the names from the batting/pitching stats
    dataframes"""
    positions = ['1','2','3','4','5','6','7','8','9']
    pos_count = 0
    for row in positions:
        
        # New data frame with split value columns 
        new = df[positions[pos_count]].str.split("-", n = 1, expand = True) 

        # Making separate name column from new data frame 
        df[positions[pos_count]] = new[0] 

        # Making separate position column from new data frame 
        df["Position"]= new[1]
        df.drop(columns = 'Position')
        pos_count += 1
        
        
# Define function for cleaning Game column
def clean_game_column(df):
    """Takes the 'Game' column in the lineups dataframe and splits teh date to make it easier to read and removes the final score"""
    new = df['0'].str.split(" ", n = 5, expand = True)
    df['Game Date'] = new[1]
    df['Opponent'] = new[3]
    df['Win Loss'] = new[4]
    new_date = df['Game Date'].str.split('/', n = 1, expand = True)
    df['Month'] = new_date[0]
    df['Date'] = new_date[1]
    new_month = df['Month'].str[3]
    df['Month'] = new_month