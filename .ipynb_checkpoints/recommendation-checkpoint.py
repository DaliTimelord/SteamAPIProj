import pandas as pd
import numpy as np
from sklearn import neighbors
KNN = neighbors.KNeighborsClassifier(metric='euclidean', n_neighbors=1)
from sklearn.model_selection import train_test_split

#input a user's steamid and the full data set. The function look up his data and drop it 


def recommendation(users_steam_id, total_data1):
    #getting the users data who were are testing a dropping it's row from the data
    total_data0 = total_data1.copy()
    users_data = total_data0.loc[total_data0['Steam_id']== int(users_steam_id)]
    total_data = total_data0.drop(users_data.index[0])
    
    #creating the labels as every users steam id, and fitting the nearest neighbors algorithm 
    labels = list(total_data['Steam_id'])
    total_data = total_data.drop(['Steam_id'],axis=1)
    nn = neighbors.KNeighborsClassifier(n_neighbors=1, metric='euclidean')
    nn.fit(total_data,labels)
    
    #predicts the user most similar to the one one who's steam id we are testing. Then pulls that row of data
    users_data = users_data.drop(['Steam_id'], axis=1)
    users_data = users_data.values[0]
    similar_user = nn.predict([users_data])
    similar_user = str(similar_user[0])
    similar_user_data = total_data0.query('Steam_id == ' + similar_user)
    similar_user_data = similar_user_data.drop(['Steam_id'], axis=1)

    #Need the users data as a dataframe
    users_full_data = total_data0.query('Steam_id == ' + users_steam_id)
    users_full_data = users_full_data.drop(['Steam_id'], axis=1)

    #get a list of the column names
    column_labels = list(total_data0.columns)
    column_labels = column_labels[1:]

    #Used to compare the data of the user and the similar user and get only the games the similar user has and the inputted user doesn't
    similar_user_column_list = []
    users_column_list = []

    for i in (column_labels):
        one_game_sim_user = int(similar_user_data[str(i)].values[0])
        one_game_user = int(users_full_data[str(i)].values[0])

        if one_game_sim_user > 0 & one_game_user < 1:
            similar_user_column = str(i)
            users_column = str(i)
            similar_user_column_list.append(similar_user_column)
            users_column_list.append(users_column)

    similar_user_data = similar_user_data[similar_user_column_list]
    users_full_data = users_full_data[users_column_list]

    #used as a double check incase it didn't get rid of all the user's values > 0
    for i in (users_full_data):
        one_game_user2 = int(users_full_data[str(i)].values[0])
        if one_game_user2 != 0:
            users_full_data = users_full_data.drop([str(i)], axis = 1)
            similar_user_data = similar_user_data.drop([str(i)], axis = 1)

    #finds the game that is most played by the similar user and the user we are testing for doesn't have
    game_suggestion = 0

    for i in (similar_user_data):
        one_game_sim_user2 = int(similar_user_data[str(i)].values[0])   

        if one_game_sim_user2 > game_suggestion:
            game_suggestion = one_game_sim_user2
            final_suggestion = i 

    return final_suggestion