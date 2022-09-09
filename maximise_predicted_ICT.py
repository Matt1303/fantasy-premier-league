def maximise_predicted_ICT(min_gameweek, 
                           max_gameweek,
                           split_by_gameweek=True,
                           minimum_chance_of_playing=default_minimum_chance_of_playing,
                           budget=100,
                           formation=None,
                           current_team_count=None,
                           players_to_exclude=None):
    '''Calculate optimum team for gameweek(s) defined by min_gameweek and max_gameweek, by gameweek, subject to the
    defined budget and formation (in the form number of players split by a dash, i.e. GK-DEF-MID-FWD)'''
    
    budget = budget/10
    
    all_data=linear_regression_predictions(min_gameweek=min_gameweek, max_gameweek=max_gameweek)
    
    # average the individual GW data if not splitting by GW 
    if split_by_gameweek==False:
        grouped_data = (all_data.groupby('name').mean()
                    .sort_values('Predicted ICT', ascending=False)
                    [['now_cost', 'chance_of_playing_next_round', 'Predicted ICT']])
        
        # merge with all_data to add non numeric fields to grouped_data
        grouped_data = grouped_data.merge(all_data[['name', 'position', 'team name']], how='left', on='name').drop_duplicates().reset_index(drop=True)
        
        all_data = (grouped_data[grouped_data['chance_of_playing_next_round'] >= minimum_chance_of_playing])

    
    #alL_total_predicted_ICT
    
    optimum_team_by_gw = pd.DataFrame(columns=['name', 'position', 'now_cost', 'chance_of_playing_next_round',
       'kickoff_time', 'GW', 'team name', 'opponent team name',
       'team_strength_diff', 'rolling_avg_ict', 'Predicted ICT'])
    
    if split_by_gameweek==True:
        for gw in range(min_gameweek, max_gameweek+1):
            data = all_data[all_data['GW']==gw] # perform team optimisation for each GW

            # remove players with a chance of playing less than minimum_chance_of_playing
            data = (data[data['chance_of_playing_next_round'] >= minimum_chance_of_playing])

            # if formation defined, pass this into linear_optimisation function 
            if formation != None:        
                optimum_team = linear_optimisation(player_data=data, budget=budget, formation=formation, current_team_count=current_team_count, players_to_exclude=players_to_exclude)
                optimum_team_by_gw = pd.concat([optimum_team_by_gw, optimum_team[0]])
                
            optimum_team_by_gw = pd.concat([optimum_team_by_gw, 
                                            find_optimum_formation(player_data=data, budget=budget, current_team_count=current_team_count, players_to_exclude=players_to_exclude, gw=gw)])
        
        
    if split_by_gameweek==False:

        # if formation defined, pass this into linear_optimisation function 
        if formation != None:        
            optimum_team = linear_optimisation(player_data=all_data, budget=budget, formation=formation, current_team_count=current_team_count, players_to_exclude=players_to_exclude)
            optimum_team_by_gw = pd.concat([optimum_team_by_gw, optimum_team[0]])
            return optimum_team_by_gw
            
        optimum_team_by_gw = find_optimum_formation(player_data=all_data, budget=budget, current_team_count=current_team_count, players_to_exclude=players_to_exclude)
        optimum_team_by_gw.reset_index(drop=False, inplace=True)
        optimum_team_by_gw.rename(columns={'index': 'player rank'}, inplace=True) # the index is the position of the player ordered by Predicted ICT descending
        optimum_team_by_gw['player rank'] = optimum_team_by_gw['player rank']+1

    return optimum_team_by_gw