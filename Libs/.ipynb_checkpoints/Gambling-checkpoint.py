import pandas as pd
from path import Path

def find_total_profits(df, bet_amount, year):
    # Convert open odds to integers
    df['Home_Open_Odds'] = df['Home_Open_Odds'].astype(int)
    df['Visitor_Open_Odds'] = df['Visitor_Open_Odds'].astype(int)
    bet_amount = int(bet_amount)

    # Pull in predicted win and predicted loss
    home_win = df[df['Predicted'] == 1]
    home_loss = df[df['Predicted'] == 0]


    # Grab instances where the predicted winner is the favorite to win
    home_win_fav = home_win[home_win['Home_Open_Odds'] < 0]
    home_loss_fav = home_loss[home_loss['Visitor_Open_Odds'] < 0]


    # Grab instances where the predicted winner is the underdog
    home_win_dog = home_win[home_win['Home_Open_Odds'] > 0]
    home_loss_dog = home_loss[home_loss['Visitor_Open_Odds'] > 0]


    # Grab instances where the favs were the actual winners and predicted winners
    home_win_fav_true = home_win_fav[home_win_fav['Actual'] == 1]
    #home_win_fav_true['Home_Open_Odds'] = ((10000)/abs(home_win_fav_true['Home_Open_Odds']))
    home_win_fav_true['Home_Open_Odds'] = ((bet_amount)/(abs(home_win_fav_true['Home_Open_Odds'])/100))
    home_loss_fav_true = home_loss_fav[home_loss_fav['Actual'] == 0]
    #home_loss_fav_true['Visitor_Open_Odds'] = ((10000)/abs(home_loss_fav_true['Visitor_Open_Odds']))
    home_loss_fav_true['Visitor_Open_Odds'] = ((bet_amount)/(abs(home_loss_fav_true['Visitor_Open_Odds'])/100))



    # Grab instances where the dogs were winners and predicted winners
    home_win_dog_true = home_win_dog[home_win_dog['Actual'] == 1]
    home_win_dog_true['Home_Open_Odds'] = home_win_dog_true['Home_Open_Odds']*(bet_amount/100)
    home_loss_dog_true = home_loss_dog[home_loss_dog['Actual'] == 0]
    home_loss_dog_true['Visitor_Open_Odds'] = home_loss_dog_true['Visitor_Open_Odds']*(bet_amount/100)


    # Grab instances where the dogs were losers, but predicted winners
    home_win_dog_false = home_win_dog[home_win_dog['Actual'] == 0]
    home_loss_dog_false = home_loss_dog[home_loss_dog['Actual'] == 1]

    # Grab instances where the favs were predicted winners but lost
    home_win_fav_false = home_win_fav[home_win_fav['Actual'] == 0]
    home_win_fav_false['Home_Open_Odds'] = -(bet_amount)
    home_loss_fav_false = home_loss_fav[home_loss_fav['Actual'] == 1]
    home_loss_fav_false['Visitor_Open_Odds'] = -(bet_amount)

    # Grab instances where the dgos were predicted winners but lost
    home_win_dog_false['Home_Open_Odds'] = -(bet_amount)
    home_loss_dog_false['Visitor_Open_Odds'] = -(bet_amount)

    # Concatinate the dataframes
    bet_results_fav_win = pd.concat([home_win_fav_false, home_win_fav_true]) # Home Open Odds
    bet_results_fav_win.sort_index(inplace = True)
    bet_results_fav_loss = pd.concat([home_loss_fav_false, home_loss_fav_true]) # Visitor Open Odds
    bet_results_fav_loss.sort_index(inplace = True)
    bet_results_dog_win = pd.concat([home_win_dog_true, home_win_dog_false]) # Home Open Odds
    bet_results_dog_win.sort_index(inplace = True)
    bet_results_dog_loss = pd.concat([home_loss_dog_true, home_loss_dog_false]) # Visitor Open Odds
    bet_results_dog_loss.sort_index(inplace = True)
    
    # Calculate cumulative sum for each of the betting results
    cum_sum_fav_win = bet_results_fav_win['Home_Open_Odds'].cumsum()
    cum_sum_fav_loss = bet_results_fav_loss['Visitor_Open_Odds'].cumsum()
    cum_sum_dog_win = bet_results_dog_win['Home_Open_Odds'].cumsum()
    cum_sum_dog_loss = bet_results_dog_loss['Visitor_Open_Odds'].cumsum()

   
    # Determine the accuracy of each of the four betting methods
    fav_win_win_len = len(home_win_fav_true)
    fav_win_tot_len = len(bet_results_fav_win)
    fav_win_acc = round(100*(fav_win_win_len/fav_win_tot_len),2)
    fav_loss_win_len = len(home_loss_fav_true)
    fav_loss_tot_len = len(bet_results_fav_loss)
    fav_loss_acc = round(100*(fav_loss_win_len/fav_loss_tot_len),2)
    dog_win_win_len = len(home_win_dog_true)
    dog_win_tot_len = len(bet_results_dog_win)
    dog_win_acc = round(100*(dog_win_win_len/dog_win_tot_len),2)
    dog_loss_win_len = len(home_loss_dog_true)
    dog_loss_tot_len = len(bet_results_dog_loss)
    dog_loss_acc = round(100*(dog_loss_win_len/dog_loss_tot_len),2)

    # Sum up final wins/loss money lines
    fav_win_sum = round(bet_results_fav_win['Home_Open_Odds'].sum(),2)
    fav_loss_sum = round(bet_results_fav_loss['Visitor_Open_Odds'].sum(),2)
    dog_win_sum = round(bet_results_dog_win['Home_Open_Odds'].sum(),2)
    dog_loss_sum = round(bet_results_dog_loss['Visitor_Open_Odds'].sum(),2)
    final_sum = round(fav_win_sum + fav_loss_sum + dog_win_sum + dog_loss_sum,2)
    print(f'Betting on the favorites to win at home: ${fav_win_sum}\nThe accuracy of betting on the favorites to win at home is {fav_win_acc}%\nThe number of games that would have been bet on is {len(bet_results_fav_win)}\nBetting on the favorites to win on the road: ${fav_loss_sum}\nThe accuracy of betting on the favorites to win on the road is {fav_loss_acc}%\nThe number of games that would have been bet on is {len(bet_results_fav_loss)}\nBetting on the underdogs to win at home: ${dog_win_sum}\nThe accuracy of betting on the underdogs to win at home is {dog_win_acc}%\nThe number of games that would have been bet on is {len(bet_results_dog_win)}\nBetting on the dogs to win on the road: ${dog_loss_sum}\nThe accuracy of betting on the underdogs to win on the road is {dog_loss_acc}%\nThe number of games that would have been bet on is {len(bet_results_dog_loss)}\nTotal profits for the second half of the {year} season: ${final_sum}\n\n\n')