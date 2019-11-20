import pandas as pd

def dog_strategy(df):
    """This function will take the predictions vs actual dataframe that resulted from our RandomForestClassifier model.  It will return a dataframe detailing the profit/loss of our gambling
       strategy of only betting on underdogs that our model predicts to win."""

    winner = []
    loser = []
    prediction = []
    date = []
    previous_bankroll = [1000]
    current_bankroll = [1000]
    profit_loss = [0]
    current_bet = [0]
    total_profit_loss = [0]
    total_winnings = [0]
    
    for index, row in df.iterrows():
        if row['Home_Open_Odds'] > 0 and row['Predicted'] == 1:
            if row['Actual'] == row['Predicted']:
                current_bet.append(100)
                previous_bankroll.append(current_bankroll[-1])
                profit_loss.append(row['Home_Open_Odds'])
                total_profit_loss.append(total_profit_loss[-1] + profit_loss[-1])
                current_bankroll.append(previous_bankroll[-1] + profit_loss[-1])
                date.append(index)
                winner.append(row['Home'])
                loser.append(row['Visitor'])
                prediction.append(row['Home'])
            else:
                current_bet.append(100)
                previous_bankroll.append(current_bankroll[-1])
                profit_loss.append(-100)
                total_profit_loss.append(total_profit_loss[-1] + profit_loss[-1])
                current_bankroll.append(previous_bankroll[-1] + profit_loss[-1])
                date.append(index)
                winner.append(row['Visitor'])
                loser.append(row['Home'])
                prediction.append(row['Visitor'])
        elif row['Visitor_Open_Odds'] > 0 and row['Predicted'] == 0:
            if row['Actual'] == row['Predicted']:
                current_bet.append(100)
                previous_bankroll.append(current_bankroll[-1])
                profit_loss.append(row['Visitor_Open_Odds'])
                total_profit_loss.append(total_profit_loss[-1] + profit_loss[-1])
                current_bankroll.append(previous_bankroll[-1] + profit_loss[-1])
                date.append(index)
                winner.append(row['Visitor'])
                loser.append(row['Home'])
                prediction.append(row['Visitor'])
            else:
                current_bet.append(100)
                previous_bankroll.append(current_bankroll[-1])
                profit_loss.append(-100)
                total_profit_loss.append(total_profit_loss[-1] + profit_loss[-1])
                current_bankroll.append(previous_bankroll[-1] + profit_loss[-1])
                date.append(index)
                winner.append(row['Home'])
                loser.append(row['Visitor'])
                prediction.append(row['Visitor'])
    results_df = pd.DataFrame([date, winner, loser, prediction, current_bet[1:], previous_bankroll[1:], profit_loss[1:], total_profit_loss[1:], current_bankroll[1:]]).T
    results_df.columns = ['Date', 'Winner', 'Loser', 'Prediction', 'Current_Bet', 'Previous_Bankroll', 'Profit_Loss', 'Total_Profit_Loss', 'Current_Bankroll']
    results_df = results_df.set_index('Date')
    return results_df