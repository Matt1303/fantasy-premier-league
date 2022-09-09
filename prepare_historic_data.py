def prepare_historic_data(min_minutes_played = 10, form_window=default_form_window, minimum_game_window=2):
    '''Clean and combine data from past few seasons for use in the linear regression model.
        o define min_minutes_played to remove data where players played fewer minutes than this
        o define form_window to specify the number of recent games to use to calculate average recent ICT
        o define minimum_game_window to specify the minimum number of games played by a player in the given season 
          to average over (must be less than or equal to form_window)'''
    
    seasons = ['2018-19',
            '2019-20',
            '2020-21',
            '2021-22',
            '2022-23'  # include current season
            ]

    data = pd.read_csv(folder_location+fr'\Fantasy-Premier-League\data\cleaned_merged_seasons.csv')
    
    data = data[~data['season_x'].isin(['2016-17', '2017-18'])] # remove these two seasons as not all data needed is available for them 

    teams_by_season = pd.DataFrame(columns=['season', 'id', 'name', 'strength_overall_home', 'strength_overall_away'])
    fixtures_by_season = pd.DataFrame(columns=['season','id', 'team_h', 'team_a'])

    for season in seasons:
        teams = pd.read_csv(folder_location+fr'\Fantasy-Premier-League\data\{season}\teams.csv')
        teams['season']=season
        teams = teams[['season', 'id', 'name', 'strength_overall_home', 'strength_overall_away']]
        teams_by_season = pd.concat([teams_by_season, teams])

        fixtures = pd.read_csv(folder_location+fr'\Fantasy-Premier-League\data\{season}\fixtures.csv')
        fixtures['season']=season
        fixtures = fixtures[['season', 'id', 'team_h', 'team_a']]
        fixtures_by_season = pd.concat([fixtures_by_season, fixtures])

    combined_data = data.merge(teams_by_season[['season', 'id', 'strength_overall_home', 'strength_overall_away']], 
                    how='left',
                    left_on=['season_x', 'opponent_team'],
                    right_on=['season', 'id'])

    combined_data['opponent strength'] = np.where(combined_data['was_home']==True,
                                                combined_data['strength_overall_away'], 
                                                combined_data['strength_overall_home'])

    combined_data.drop(['season', 'id', 'strength_overall_away','strength_overall_home'], 
                        axis=1,
                        inplace=True)

    combined_data.rename({'season_x': 'season',
                        'team_x': 'team'},
                        axis=1,
                        inplace=True)

    combined_data = combined_data.merge(fixtures_by_season, 
                    how='left',
                    left_on=['season', 'fixture'],
                    right_on=['season', 'id'])

    combined_data['team id'] = np.where(combined_data['was_home']==True,
                                        combined_data['team_h'], 
                                        combined_data['team_a'])
    
    
    combined_data.drop(['team_h','team_a', 'id'], 
                       axis=1,
                       inplace=True)
    
    combined_data = combined_data.merge(teams_by_season[['season', 'id', 'strength_overall_home', 'strength_overall_away']], 
                    how='left',
                    left_on=['season', 'team id'],
                    right_on=['season', 'id'])
    
    combined_data['team strength'] = np.where(combined_data['was_home']==True,
                                                combined_data['strength_overall_home'], 
                                                combined_data['strength_overall_away'])
    
    combined_data.drop(['id', 'strength_overall_away','strength_overall_home'], 
                        axis=1,
                        inplace=True)
    
    combined_data['team_strength_diff'] = combined_data['team strength']-combined_data['opponent strength']
    
    combined_data.sort_values(['name', 'season', 'fixture'], ascending=True, inplace=True)
    
    combined_data['rolling_avg_ict'] = combined_data.groupby(['name', 'season'])['ict_index'].transform(lambda x: x.rolling(window=form_window, 
                                                                                                                            min_periods=minimum_game_window, 
                                                                                                                            axis=0, 
                                                                                                                            closed='left').mean())
    
    combined_data = combined_data[combined_data['minutes'] > min_minutes_played] # remove matches where the player barely played 
    
    combined_data = combined_data[['season', 'fixture', 'name', 'ict_index', 'team_strength_diff', 'rolling_avg_ict', 'position', 'creativity', 'influence', 'threat', 'value']].reset_index(drop=True)
    
    return combined_data