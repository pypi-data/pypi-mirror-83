import pandas as pd
import numpy as np
from sklearn.model_selection import cross_validate
from sklearn.model_selection import cross_val_score
from sklearn import metrics

def modelfit(algo, train, test, predictors, target, IDcol, filename):
    #Fit the algorithm on the data
    algo.fit(train[predictors], train[target])
        
    #Predict training set:
    train_predictions = algo.predict(train[predictors])
    #Perform cross-validation:
    cv_score = cross_val_score(algo, train[predictors],(train[target]) , cv=20, scoring='neg_mean_squared_error')
    cv_score = np.sqrt(np.abs(cv_score))
    
    #Print model report:
    print("\nModel Report")
    print("RMSE : %.4g" % np.sqrt(metrics.mean_squared_error((train[target]).values, train_predictions)))
    print("CV Score : Mean - %.4g | Std - %.4g | Min - %.4g | Max - %.4g" % (np.mean(cv_score),np.std(cv_score),np.min(cv_score),np.max(cv_score)))
    
    #Predict on testing data:
    test[target] = algo.predict(test[predictors])
    
    #Export submission file:
    IDcol.append(target)
    submission = pd.DataFrame({ x: test[x] for x in IDcol})
    submission.to_csv(filename, index=False)
    
"""
Predictors=X
Target=Y
IDcol= Columns needed to make submission file
"""