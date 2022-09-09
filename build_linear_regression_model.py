def build_linear_regression_model(test_size=0.3, random_state=42, show_graphs=False, model_analysis=False):
    '''Create multiple linear regression model to predict ICT (influence, creativity, threat) metric based on recent 
       form (recent average ICT) and relative strength of the players' teams' upcoming fixture, using data from recent seasons.
           o Split the dataset into training and test datasets using the test_size argument
           o random_state parameter used to ensure repeatability of results
           o set show_graphs=True to visualise the individual simple linear regression models of the two features against the target variable
           o set model_analysis=True to output analysis of the linear regression model performance'''
    historic_data = prepare_historic_data()

    historic_data.dropna(subset=['rolling_avg_ict'], axis=0, inplace=True) # remove first two games of season where we don't yet have a rolling average ICT
    
    # two model features: team strength diff and recent ICT average
    X = historic_data.drop(['season', 'fixture', 'name', 'ict_index', 'position', 'creativity', 'influence', 'threat', 'value'], axis=1).values # create model features as numpy array
    y = historic_data['ict_index'].values # create target variable as numpy array
    
    if show_graphs==1:
        # visualise simple linear regression model fits for the two features
        for i in [0,1]:
            X_simple = X[:,i]
            X_simple = X_simple.reshape(-1,1)

            reg = LinearRegression() # Create the model
            reg.fit(X_simple,y) # Fit the model to the data
            predictions = reg.predict(X_simple) # Make predictions

            plt.figure(figsize=(15,8))
            # plot scatter plot of all points and overlay the line of best fit based on simple linear regression model
            plt.scatter(X_simple, y)
            plt.plot(X_simple, predictions, color="red")
            plt.ylabel("Actual ICT")
            plt.xlabel(np.where(i==0, "Team strength diff", "Recent average ICT"))
            plt.show()
    
    # generate multiple linear regression model using both features
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    reg = LinearRegression()
    reg.fit(X_train, y_train)
    y_pred = reg.predict(X_test)

    if model_analysis==1:      
        # analyse model performances, including Ridge and Lasso variants of the linear regression model
        
        r_squared = reg.score(X_test, y_test) # Compute R-squared
        rmse = mean_squared_error(y_test, y_pred, squared=False) # Compute RMSE       
        
        print("Multiple linear regression R^2: {}".format(r_squared))
        print("Multiple linear regression RMSE: {}".format(rmse))
                   
        alphas = [0.1, 1.0, 10.0, 100.0, 1000.0, 2000.0, 10000.0]
        ridge_scores = {}
        for alpha in alphas:
            ridge = Ridge(alpha=alpha) # create a Ridge regression model
            ridge.fit(X_train, y_train) # fit the data
            score = ridge.score(X_test, y_test) # obtain R-squared
            ridge_scores[alpha] = score # append score to dict for that value of alpha
        print(fr"Ridge scores by alpha: {ridge_scores}")
        print(fr"Best alpha to use: {max(ridge_scores, key=ridge_scores.get)}")
        
        # pass best performing alpha value into the Ridge model
        models = {"Linear Regression": LinearRegression(),
                  "Ridge": Ridge(alpha=max(ridge_scores, key=ridge_scores.get)),
                  "Lasso": Lasso(alpha=0.1)}
        results = []

        # Loop through the models' values
        for model in models.values():
            kf = KFold(n_splits=6, random_state=42, shuffle=True)
            cv_scores = cross_val_score(model, X_train, y_train, cv=kf) # perform cross-validation
            results.append(cv_scores) # append the results

        plt.boxplot(results, labels=models.keys()) # create a box plot of the results
        plt.show()
                   
        for name, model in models.items():

            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            test_rmse = mean_squared_error(y_test, y_pred, squared=False)
            print("{} Test Set RMSE: {}".format(name, test_rmse))
                   
        print(fr'Mean cross-validation score: {np.mean(cv_scores)}')
        print(fr'Standard deviation of cross-validation score: {np.std(cv_scores)}')      
        print(fr'95% confidence interval of cross-validation score: {np.quantile(cv_scores, [0.025, 0.975])}')   

    # return regression model
    return reg