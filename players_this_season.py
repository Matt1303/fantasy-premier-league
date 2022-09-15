def players_this_season(current_season = '2022-23'):
    '''Create dataframe of upcoming players this season
          o pass in current_season in the form YYYY-YY e.g. 2022-23'''

    players_this_season = pd.read_csv(folder_location+fr'\Fantasy-Premier-League\data\{current_season}\players_raw.csv', 
                           usecols=['id',
                                    'first_name',
                                    'second_name',
                                    'team',
                                    'chance_of_playing_next_round',
                                    'selected_by_percent'])
    
    players_cleaned = pd.read_csv(folder_location+fr'\Fantasy-Premier-League\data\{current_season}\cleaned_players.csv', 
                       usecols=['first_name',
                                'second_name',
                                'element_type',
                                'now_cost'])

    for df in [players_this_season, players_cleaned]:
        df['name'] = df['first_name']+' '+df['second_name']
        df.drop(['first_name', 'second_name'],axis=1, inplace=True)
    
    players_this_season_final = players_this_season.merge(players_cleaned, 
                                  on='name',
                                  how='left')

    players_this_season_final.rename({'id': 'player_id',
                                     'element_type': 'position'},
                                     axis=1,
                                     inplace=True)
    
    # remove Roberto Firmino as Nunez is back
    players_this_season_final = players_this_season_final[~players_this_season_final['name'].str.contains('Firmino')]
    
    # remove Ben Davies
    players_this_season_final = players_this_season_final[players_this_season_final['name']!='Ben Davies']
    
    return players_this_season_final[['player_id', 'name', 'team', 'position', 'now_cost', 'chance_of_playing_next_round', 'selected_by_percent']]