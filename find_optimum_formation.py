def find_optimum_formation(player_data, budget, current_team_count, players_to_exclude, gw=None):
    '''Finds the formation of 11 players which produces the highest predicted ICT, subject to the constraints 
       defined in the function arguments'''
   
    ict = None

    # optimise best formation by trying each 11 player formation and calculating resulting predict ICT for each
    for formation_to_try in ["1-5-4-1", "1-5-3-2", "1-5-2-3", "1-4-5-1", "1-4-4-2", "1-4-3-3", "1-3-5-2", "1-3-4-3"]:
        optimum_team = linear_optimisation(player_data=player_data, budget=budget, formation=formation_to_try, current_team_count=current_team_count, players_to_exclude=players_to_exclude)
        predicted_ict = optimum_team[2]
        if gw != None:
            print(fr"GW {gw} {formation_to_try}: {predicted_ict}")
        else:
            print(fr"{formation_to_try}: {predicted_ict}")
        # if the first formation tried, update the gameweek ict and optimised team
        if ict == None:
            ict=predicted_ict
            optimum_team_by_gw = optimum_team[0] #pd.concat([optimum_team_by_gw, optimum_team[0]])
        # update the ict and optimised team if found a higher scoring formation
        if predicted_ict > ict:            
            optimum_team_by_gw = optimum_team[0]
        
    print('-------------------')
                
    return optimum_team_by_gw
