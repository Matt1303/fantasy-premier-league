def this_season_data(current_season='2022-23'):
    '''Extract average ICT data for the current season'''

    this_season_data = pd.read_csv(folder_location+fr'\Fantasy-Premier-League\data\{current_season}\gws\merged_gw.csv')

    # sort by name and fixture so rolling ICT index is calculated properly
    this_season_data = this_season_data.sort_values(['name', 'fixture'], ascending=True)

    this_season_data['rolling_avg_ict'] = this_season_data.groupby('name')['ict_index'].transform(lambda x: x.rolling(window=5, 
                                                                                                                min_periods=2, 
                                                                                                                axis=0).mean())

    # keep only the most recent gameweek data
    this_season_data = this_season_data[this_season_data['GW']==this_season_data['GW'].max()]
    
    # only keep the ICT metric for use in the predictive model
    this_season_data = this_season_data[['name', 'team', 'rolling_avg_ict']]
    
    return this_season_data