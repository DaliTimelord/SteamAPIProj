import pandas as pd
import numpy as np
from sklearn import neighbors
KNN = neighbors.KNeighborsClassifier(metric='euclidean', n_neighbors=1)
from sklearn.model_selection import train_test_split


def recommendation(user_gameplay_data, total_data, labels):
    nn = neighbors.KNeighborsClassifier(n_neighbors=1, metric='euclidean')
    nn.fit(total_data,labels)
    
    users_data = user_gameplay_data.drop(['Steam_id'], axis=1).values
    similar_user = nn.predict([users_data])
    similar_user = str(similar_user[0])
    similar_user_data = total_data.query('Steam_id == ' + similar_user)
    similar_user_data = similar_user_data.drop(['Steam_id'], axis=1)
    
    
    for i in (column_labels):
        one_game_sim_user = similar_user_data[str(i)].values[0]
        one_game_user = user_gameplay_data[str(i)].values[0]
        
        if one_game_sim_user == 0 & one_game_user == 0:
            similar_user_data = similar_user_data.drop([str(i)])
            users_data = users_data.drop([str(i)])
            
        elif one_game_sim_user == 0 & one_game_user > 0:
            similar_user_data = similar_user_data.drop([str(i)])
            users_data = users_data.drop([str(i)])