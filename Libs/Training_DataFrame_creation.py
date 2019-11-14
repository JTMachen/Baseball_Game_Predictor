import pandas as pd 
from datetime import timedelta


def make_schedule_with_odds(odds_df):
    """ Takes a dataframe of gambling odds that have each team in a game on a seperate row.  Will return a dataframe
        with both teams in a game on the same row with their Open Moneyline Odds, Close Moneyline Odds,
        who won and who lost, and Starting Pitchers. """
    new_df = pd.DataFrame()
    t = odds_df.iterrows()
    date = []
    home = []
    visitor = []
    home_pitcher = []
    visitor_pitcher = []
    home_open_odds = []
    visitor_open_odds = []
    home_close_odds = []
    visitor_close_odds = []
    home_win_loss = []
    visitor_win_loss = []
    for (i, row1), (j, row2) in zip(t, t):
        date.append(i)
        home.append(row2['Team'])
        visitor.append(row1['Team'])
        home_pitcher.append(row2['Pitcher'])
        visitor_pitcher.append(row1['Pitcher'])
        home_open_odds.append(row2['Open'])
        visitor_open_odds.append(row1['Open'])
        home_close_odds.append(row2['Close'])
        visitor_close_odds.append(row1['Close'])
        if row2['Final'] > row1['Final']:
            home_win_loss.append(1)
            visitor_win_loss.append(0)
        else:
            home_win_loss.append(0)
            visitor_win_loss.append(1)
    schedule_odds_df = pd.DataFrame(list(zip(home, visitor, home_pitcher, visitor_pitcher, home_open_odds, visitor_open_odds, home_close_odds, 
              visitor_close_odds, home_win_loss, visitor_win_loss)), columns=['home','visitor', 'home_pitcher', 'visitor_pitcher', 
              'home_open_odds', 'visitor_open_odds', 'home_close_odds', 'visitor_close_odds', 'home_win_loss', 'visitor_win_loss'], 
              index = date)
    return schedule_odds_df
        
    
def stats_for_game_day(schedule_odds_df, batting_df, pitching_df, look_back):
    """ This function takes an odds_df that has been scrubbed through_schedule_with_odds, a batting_df that has been cleaned from PyBaseball,
        a pitching_df that has been cleaned from PyBaseball, and accepts an integer for a lookback period.  The lookback period is the time 
        previous to the game being played that you want to calculate teams stats for.  This function will return a tuple with the cumulative
        hitting stats for each team during the lookback period as the first value of the tuple.  The second value of the tuple will be the 
        cumulative pitching stats for each team for the lookback period."""
    
    hitting_day_list = []
    pitching_day_list = []
    for index, row in schedule_odds_df.iterrows():
        hitting_day = batting_df.loc[index - timedelta(look_back): index - timedelta(1)].groupby('Tm').sum()
        pitching_day = pitching_df.loc[index - timedelta(look_back): index - timedelta(1)].groupby('Tm').sum()
        hitting_day_list.append(hitting_day)
        pitching_day_list.append(pitching_day)
    return hitting_day_list, pitching_day_list


def df_for_feature_selection(odds_df, batting_df, pitching_df, look_back):
    """ This is the main function for this library.  Every other function is a helper function.This function takes an odds_df that has been scrubbed 
        through_schedule_with_odds, a batting_df that has been cleaned from PyBaseball, a pitching_df that has been cleaned from PyBaseball, and accepts an 
        integer for a lookback period that all stats are calculated for.  This function will return a dataframe with all the odds info, cumulative home team hitting stats, 
        cumulative home team pitching stats, cumulative visitor team hitting stats, cumulative visitor team pitching stats, and who won the game.  Each row of the 
        dataframe represents one game with the cumulative stats, odds, and winner between the 2 teams."""
    
    # Use helper function to get schedule with odds
    odds_df_with_lookback = odds_df[odds_df.index[0] + timedelta(look_back): batting_data_df.index[-1]]
    schedule_odds_df = make_schedule_with_odds(odds_df_with_lookback)
    
    # Use helper function to get all stats for lookback period by team
    hitting_day, pitching_day = stats_for_game_day(schedule_odds_df, batting_df, pitching_df, look_back)

    # Create one dataframe that houses all the odds, stats, winners and losers for each game played 
    total_df = pd.DataFrame()
    for i in range(len(schedule_odds_df)):
        hitting_day_df = pd.DataFrame(hitting_day[i])
        pitching_day_df = pd.DataFrame(pitching_day[i])
        hitting_games_home = pd.DataFrame(hitting_day_df.loc[schedule_odds_df['home'][i]]).T.reset_index().drop(columns = ['index', 'VH'])
        hitting_games_home['Date'] = schedule_odds_df.index[i]
        hitting_games_home = hitting_games_home.set_index('Date')
        hitting_games_home = hitting_games_home.add_prefix('Home_Hitting')
        hitting_games_visitor = pd.DataFrame(hitting_day_df.loc[schedule_odds_df['visitor'][i]]).T.reset_index().drop(columns = ['index', 'VH'])
        hitting_games_visitor['Date'] = schedule_odds_df.index[i]
        hitting_games_visitor = hitting_games_visitor.set_index('Date')
        hitting_games_visitor = hitting_games_visitor.add_prefix('Visitor_Hitting')
        pitching_games_home = pd.DataFrame(pitching_day_df.loc[schedule_odds_df['home'][i]]).T.reset_index().drop(columns = ['index', 'VH'])
        pitching_games_home['Date'] = schedule_odds_df.index[i]
        pitching_games_home = pitching_games_home.set_index('Date')
        pitching_games_home = pitching_games_home.add_prefix('Home_Pitching')
        pitching_games_visitor = pd.DataFrame(pitching_day_df.loc[schedule_odds_df['visitor'][i]]).T.reset_index().drop(columns = ['index', 'VH'])
        pitching_games_visitor['Date'] = schedule_odds_df.index[i]
        pitching_games_visitor = pitching_games_visitor.set_index('Date')
        pitching_games_visitor = pitching_games_visitor.add_prefix('Visitor_Pitching')
        total_line = pd.concat([hitting_games_home,hitting_games_visitor, pitching_games_home, pitching_games_visitor], axis = 1)
        total_df = total_df.append(total_line)
        print(i)
    stats_odds_df = pd.concat([schedule_odds_df,total_df], axis = 1 )
    return stats_odds_df