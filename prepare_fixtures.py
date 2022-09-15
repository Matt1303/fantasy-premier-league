def prepare_fixtures(current_season = '2022-23'):
    '''Create ordered dataframe of upcoming fixtures this season
          o pass in current_season in the form YYYY-YY e.g. 2022-23'''
    
    fixtures = pd.read_csv(folder_location+fr'\Fantasy-Premier-League\data\{current_season}\fixtures.csv')
    
    #fixtures.dropna(how='any', inplace=True) # drop the fixtures which haven't been scheduled yet
    
    fixtures.sort_values('kickoff_time', ascending=True, inplace=True)
    
    # add gameweeks as column to fixtures
#     gw = pd.Series(data=range(1,39))
#     gw_final = gw.repeat(10)
#     gw_final.reset_index(drop=True, inplace=True)
    fixtures['GW'] = fixtures['event']
    
    teams_by_season = pd.DataFrame(columns=['season', 'id', 'name', 'strength_overall_home', 'strength_overall_away'])

    seasons = ['2018-19',
        '2019-20',
        '2020-21',
        '2021-22',
        '2022-23'  # include current season
        ]

    for season in seasons:
        teams = pd.read_csv(folder_location+fr'\Fantasy-Premier-League\data\{season}\teams.csv')
        teams['season']=season
        teams = teams[['season', 'id', 'name', 'strength_overall_home', 'strength_overall_away']]
        teams_by_season = pd.concat([teams_by_season, teams])

    fixtures_final = (((fixtures.merge(teams_by_season[teams_by_season['season']==current_season][['id', 'name', 'strength_overall_home']], 
                                    how='left',
                                    left_on='team_h',
                                    right_on='id')
                        .merge(teams_by_season[teams_by_season['season']==current_season][['id', 'name', 'strength_overall_away']], 
                                    how='left',
                                    left_on='team_a',
                                    right_on='id'))))

    fixtures_final.rename({'name_x': 'home_team',
                             'strength_overall_away': 'away_team_strength',
                             'name_y': 'away_team',
                             'strength_overall_home': 'home_team_strength',
                             'id_x': 'fixture'},
                              axis=1,
                              inplace=True)
    
    fixtures_final['home_team_strength_diff'] = fixtures_final['home_team_strength']-fixtures_final['away_team_strength']
    fixtures_final['away_team_strength_diff'] = fixtures_final['away_team_strength']-fixtures_final['home_team_strength']

    fixtures_final.drop(['id_y', 'id'], axis=1, inplace=True)  
    
    return fixtures_final[['fixture',
                           'kickoff_time',
                           'team_h', 
                           'home_team', 
                           'home_team_strength_diff',
                           'team_a', 
                           'away_team', 
                           'away_team_strength_diff',
                           'GW']].sort_values('kickoff_time', ascending=True)#.head(100)