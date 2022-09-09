def fixtures_and_form():
    '''Merge the two dataframes containing the features (team strength diff and average recent ICT) to be used 
    by the regression model'''
    fixtures_and_form = fixtures_this_season().merge(this_season_data(),   #latest_form
                                             how='left',
                                             left_on=['name', 'team name'],
                                             right_on=['name', 'team'])
                                             #right_index=True)   #right_index=True

    missing_names = pd.DataFrame(fixtures_and_form[fixtures_and_form['rolling_avg_ict'].isna()]['name'].unique(),
                                 columns=['Missing player names'])
    
    if len(missing_names) > 0:
        print(fr"List of players dropped from dataset as no join between final_fixtures and this_season_data on name and team (or newly transferred players without enough ICT data): {missing_names.values}")

    return fixtures_and_form