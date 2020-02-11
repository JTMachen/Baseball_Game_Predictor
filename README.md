# Better Batter Bettors

## Overview

 - Using the pybaseball API, we pulled various statistics for each player for each game that they played in, separated them by team, and compared the previous week's stats for each team playing against each other for every game after the first week of the season.

 - We then ran through several machine learning models, training the models on the first half of the 2017, 2018, and 2019 seasons.

 - Using the training models, we tested them on the latter half of each of the three seasons.

 - Since the season had already ended when we began testing, we compared the predictions of our models to the results of the games that had occured.

 - Using those predictions, we wanted to see how much money we would have won/lost if we had placed the same bet amount on each of the predicted winners.

 - We pulled in all of the betting odds for the three seasons and calculated how much money we made/lost, compiling them into various graphs based on different betting odds, i.e. betting solely on the underdogs, betting only on the favorites, etc.


## Technologies Used

 - Jupyter-Notebook
 - Python
 - pybaseball