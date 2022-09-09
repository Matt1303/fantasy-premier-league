def top_ranked_players(min_gameweek, max_gameweek, number=100):
    '''Returns the top number of players ranked by their average predicted ICT over the defined gameweek range'''

    preds = linear_regression_predictions(min_gameweek=min_gameweek, max_gameweek=max_gameweek)

    grouped_data = preds.groupby('name').mean().sort_values('Predicted ICT', ascending=False)[['now_cost', 'chance_of_playing_next_round', 'Predicted ICT', 'selected_by_percent']].reset_index(drop=False)

    grouped_data = grouped_data.merge(preds[['name', 'position', 'team name']], how='left', on='name').drop_duplicates().reset_index(drop=True)

    grouped_data.reset_index(drop=False, inplace=True)
    grouped_data.rename(columns={'index': 'player rank'}, inplace=True) # the index is the position of the player ordered by Predicted ICT descending
    grouped_data['player rank'] = grouped_data['player rank']+1

    return grouped_data.head(number)