def fixtures_this_season():
    '''Create dataframe of fixtures this season. Note that any mismatch in names for a player outputted in 
    fixtures_this_season() and this_season_data() are corrected at the end of this function'''   

    players = players_this_season()
    fixture_list = prepare_fixtures()

    home_fixtures = (((players.merge(fixture_list[['fixture', 'kickoff_time', 'team_h', 'home_team', 'home_team_strength_diff', 'away_team', 'GW']], 
                          left_on='team',
                          right_on='team_h',
                          how='left'))))


    home_fixtures.rename({'team_h': 'team_id',
                        'home_team': 'team name',
                        'away_team': 'opponent team name',
                        'home_team_strength_diff': 'team_strength_diff'},
                        axis=1,
                        inplace=True)

    away_fixtures = (((players.merge(fixture_list[['fixture', 'kickoff_time', 'team_a', 'away_team', 'away_team_strength_diff', 'home_team', 'GW']], 
                      left_on='team',
                      right_on='team_a',
                      how='left'))))

    away_fixtures.rename({'team_a': 'team_id',
                        'away_team': 'team name',
                        'home_team': 'opponent team name',
                        'away_team_strength_diff': 'team_strength_diff'},
                        axis=1,
                        inplace=True)
    
    final_fixtures = pd.concat([home_fixtures, away_fixtures]).sort_values(['team_id',
                                                                        'name',
                                                                        'kickoff_time']).reset_index(drop=True)

    final_fixtures.drop('team', inplace=True, axis=1)
    
    # Haaland is the only player spelt differently in the two dataframes
    final_fixtures.replace(to_replace='Erling Håland', value='Erling Haaland', inplace=True)
    
    return final_fixtures