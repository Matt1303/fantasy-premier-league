def linear_regression_predictions(min_gameweek=None, max_gameweek=None):
    '''Returns dataframe containing predicted ICT based on the results of the linear regression 
    model for each player for all upcoming fixtures, unless the optional min_gameweek and/or 
    max_gameweek arguments are defined to filter the data'''

    inputs = fixtures_and_form()

    model_input = inputs[['team_strength_diff', 'rolling_avg_ict', 'GW']]
    model_input.dropna(inplace=True)   # include GW then drop where GW is null (not scheduled yet)
    model_input = model_input[['team_strength_diff', 'rolling_avg_ict']]
  
    # need to drop null ICT data from fixtures_and_form as well in order to preserve order of dataframe when concatenating with the predicted points
    inputs.dropna(inplace=True)
    inputs.reset_index(drop=True, inplace=True)
    
    X_actual = model_input.values
    predictions = build_linear_regression_model().predict(X_actual)
    
    if len(inputs) != len(predictions):
        return print("Length of input data and predictions data do not match (predicted ICT will be misaligned)")
    
    model_output = pd.concat([inputs, pd.DataFrame(predictions, columns=['Predicted ICT'])], axis=1)
    
    model_output = model_output[['name', 'position', 'now_cost', 'chance_of_playing_next_round', 'selected_by_percent','kickoff_time', 'GW', 'team name', 'opponent team name', 'team_strength_diff', 'rolling_avg_ict', 'Predicted ICT']]
    model_output['kickoff_time'] = model_output['kickoff_time'].astype(np.datetime64)
    
    future_fixtures = model_output[model_output['kickoff_time'] > pd.to_datetime('now')]
    
    # filter the data based on min_gameweek and max_gameweek if defined
    try:
        future_fixtures = future_fixtures[future_fixtures['GW'] >= min_gameweek]
    except:
        pass
    
    try:
        future_fixtures = future_fixtures[future_fixtures['GW'] <= max_gameweek]
    except:
        pass
    
    # replace 'None' with 1 to reflect no injury news for the player, and convert column to float
    future_fixtures['chance_of_playing_next_round'].replace('None', 100, inplace=True)
    future_fixtures['chance_of_playing_next_round'] = future_fixtures['chance_of_playing_next_round'].astype(float)
    
    future_fixtures['now_cost']=(future_fixtures['now_cost']/10)
    
    # return future fixtures only
    return future_fixtures.sort_values(['Predicted ICT'],ascending=False)#[future_fixtures['name']=='Erling Haaland']
