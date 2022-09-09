def current_team_ICT(player_data, current_team):

    '''Returns predicted ICT of current team using following input arguments:
         o  player_data: output from linear_regression_predictions
         o  current_team: list of player name'''
    
    # filter player_data for current_team
    current_team_data = player_data[player_data['name'].isin(current_team)]
       
    current_team_data['Predicted ICT per Cost'] = (current_team_data['Predicted ICT']/current_team_data['now_cost'])*10
    current_team_data.sort_values('Predicted ICT per Cost', ascending=False, inplace=True)

    return (current_team_data,
             round(current_team_data['Predicted ICT'].sum(),2))