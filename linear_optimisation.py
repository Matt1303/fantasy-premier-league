def linear_optimisation(player_data, 
                        num_transfers=1,                        
                        budget=None, 
                        formation=None,                       
                        current_team=None,
                        current_team_count=None, 
                        players_to_exclude=None):

    '''Optimises team using linear programming, subject to the constraints defined in the function arguemnts:
     
        optional input parameter types:
             o current_team_count: dictionary
             o players_to_exclude: list
             o current_team: dataframe containing name, now_cost, position; ordered by predicted ICT per cost, descending'''
    
    # remove players_to_exclude from player_data
    if players_to_exclude!=None:
        player_data = player_data[~player_data['name'].isin(players_to_exclude)]
        #player_data = [x for x in names if x not in players_to_exclude]
        
    if isinstance(current_team, pd.DataFrame):
        # if current_team defined, remove these players from dataset so they aren't selected again
        player_data = player_data[~player_data['name'].isin(current_team['name'])]
        
        # need to know positions and value of player(s) being transferred
        transferred_players = current_team[(len(current_team) - num_transfers):]
        if budget==None:
            budget = (transferred_players['now_cost'].sum())/10   # divide by 10 as multiply by 10 later on
        
        # remove the worst performing number of players from the current_team (equal to the num_transfers)
        current_team = current_team[:-num_transfers] # current_team is ordered by predicted ICT per cost descending so remove last players
        
        if current_team_count==None:
            current_team_count={}

            for team in current_team['team name']:
             # for any teams without a player in the squad, add the team to the dictionary with a value of zero            
                if current_team_count.get(team)==None:
                    current_team_count[team] = 0
                current_team_count[team] = current_team_count.get(team)+1
    
    # Helper variables
    POS = player_data.position.unique()
    CLUBS = player_data['team name'].unique()
    BUDGET = budget*10
    
    if isinstance(current_team, pd.DataFrame): #current_team.empty==False):
        if formation==None:

            # count number of players transferred by position
            transferred_positions = transferred_players.groupby('position').count()['name']

            # add other positions to dataframe with a value of zero in order to construct the formation string
            for position in ["GK", "DEF", "MID", "FWD"]:
                try:
                    transferred_positions[position]
                except:
                    transferred_positions[position]=0

            # create formation string based on positions of transferred_players
            formation = str(transferred_positions['GK'])+'-'+str(transferred_positions['DEF'])+'-'+str(transferred_positions['MID'])+'-'+str(transferred_positions['FWD'])

    # use formation argument if it has been specified
    pos_available = {
        'GK': int((formation.split("-"))[0]),
        'DEF': int((formation.split("-"))[1]),            
        'MID': int((formation.split("-"))[2]),            
        'FWD': int((formation.split("-"))[3]),
    }
    
    # Initialize Variables
    names = [player_data.name[i] for i in player_data.index]
    teams = [player_data['team name'][i] for i in player_data.index]
    positions = [player_data.position[i] for i in player_data.index]
    prices = [player_data['now_cost'][i] for i in player_data.index]
    points = [player_data['Predicted ICT'][i] for i in player_data.index]
    players = [LpVariable("player_" + str(i), cat="Binary") for i in player_data.index]

    prob = LpProblem("FPL Player Choices GW", LpMaximize)
    # Define the objective
    prob += lpSum(players[i] * points[i] for i in range(len(player_data))) # Objective

    # Build the constraints
    prob += lpSum(players[i] * player_data['now_cost'][player_data.index[i]] for i in range(len(player_data))) <= BUDGET # Budget Limit

    for pos in POS:
        prob += lpSum(players[i] for i in range(len(player_data)) if positions[i] == pos) == pos_available[pos] # Position Limit

    # if current_team_count defined, customise the CLUBS restraint below to account for players already in squad   
    if current_team_count==None:
        current_team_count = {} # create empty dictionary to add teams to if current_team_count not defined  
      
    for team in CLUBS:
     # for any teams without a player in the squad, add the team to the dictionary with a value of zero            
        if current_team_count.get(team)==None:
            current_team_count[team] = 0
        
    for club in CLUBS:
        prob += lpSum(players[i] for i in range(len(player_data)) if teams[i] == club) <= (3 - current_team_count.get(club)) # Club Limit

    # Solve the problem
    prob.solve()

    optimum_player_names = []
    optimum_team_names = []

    # add optimum players to optimum_player_names list
    for v in prob.variables():
        if v.varValue != 0:
            name = player_data['name'][int(v.name.split("_")[1])]
            team = player_data['team name'][int(v.name.split("_")[1])]
            optimum_player_names.append(name)
            optimum_team_names.append(team)

    # create dataframe of data for the optimum_player_names, ensuring the right player is picked and not a namesake in another club
    optimum_team = player_data[((player_data['name'].isin(optimum_player_names) & 
                                (player_data['team name'].isin(optimum_team_names))))]

    # specify bespoke order for position column
    optimum_team['position'] = pd.Categorical(optimum_team['position'],categories=['GK','DEF','MID','FWD'],ordered=True)

    try:
        optimum_team.sort_values(['GW', 'position', 'now_cost', 'Predicted ICT'],
                             ascending=[True, True, False, False],
                             inplace=True)
        
    except:
        optimum_team.sort_values(['position', 'now_cost', 'Predicted ICT'],
                             ascending=[True, False, False],
                             inplace=True)

    # calculate total predicted ICT and print this value (to compare different formations)
    total_predicted_ICT = 0

    for v in prob.variables():
        if v.varValue != 0:
            ict = player_data['Predicted ICT'][int(v.name.split("_")[1])]
            total_predicted_ICT = total_predicted_ICT+ict

    formation = (str(pos_available['GK'])+'-'+str(pos_available['DEF'])+'-'+str(pos_available['MID'])+'-'+str(pos_available['FWD']))

    
    if isinstance(current_team, pd.DataFrame):
            return (optimum_team,
             formation,
             round(total_predicted_ICT,2),
             transferred_players)
    
    return (optimum_team,
             formation,
             round(total_predicted_ICT,2))