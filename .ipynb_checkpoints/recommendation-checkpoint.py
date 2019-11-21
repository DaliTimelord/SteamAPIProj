import pandas as pd
import numpy as np
from sklearn import neighbors
KNN = neighbors.KNeighborsClassifier(metric='euclidean', n_neighbors=1)
from sklearn.model_selection import train_test_split

#input a user's steamid look up his data and drop it 


def recommendation(users_steam_id, total_data0):
    users_data = total_data0.loc[total_data0['Steam_id']== int(users_steam_id)]
    total_data = total_data0.drop(users_data.index[0])
    labels = list(total_data['Steam_id'])
    total_data = total_data.drop(['Steam_id'],axis=1)
    nn = neighbors.KNeighborsClassifier(n_neighbors=1, metric='euclidean')
    nn.fit(total_data,labels)
    users_data = users_data.drop(['Steam_id'], axis=1)
    users_data = users_data.values[0]
    similar_user = nn.predict([users_data])
    similar_user = str(similar_user[0])
    similar_user_data = total_data0.query('Steam_id == ' + similar_user)
    similar_user_data = similar_user_data.drop(['Steam_id'], axis=1)

    users_full_data = total_data0.query('Steam_id == ' + users_steam_id)

    column_labels = list(total_data0.columns)
    column_labels = column_labels[1:]

    for i in (column_labels):
        one_game_sim_user = int(similar_user_data[str(i)].values[0])
        one_game_user = int(users_full_data[str(i)].values[0])

        if one_game_sim_user == 0 & one_game_user == 0:
                similar_user_data = similar_user_data.drop([str(i)], axis = 1 )
                users_data = users_full_data.drop([str(i)], axis = 1)

        elif one_game_sim_user == 0 & one_game_user > 0:
                similar_user_data = similar_user_data.drop([str(i)], axis = 1)
                users_data = total_data0.drop([str(i)], axis =1)
                
    game_suggestion = 0
    for i in (similar_user_data):
        one_game_sim_user2 = int(similar_user_data[str(i)].values[0])   

        if one_game_sim_user2 > game_suggestion:
            game_suggestion = one_game_sim_user2
            final_suggestion = i 

    return final_suggestion