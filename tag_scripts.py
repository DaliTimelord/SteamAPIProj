import random
import pandas as pd
import numpy as np
import sklearn
from sklearn.neighbors import NearestNeighbors

def get_converted_tag_data(game_data):
    tags = game_data.tags.unique()
    tags_as_nums = {}
    count = 0
    for tag in tags:
        tags_as_nums[tag] = count
        count += 1

    game_ids = list(game_data.Game_ID.unique())
    game_names = []
    game_ids_final = []
    game_tags = []
    game_ratings = []
    
    grouped = game_data.groupby('Game_ID')

    for x in range(len(game_ids)):
        grouped_game = grouped.get_group(game_ids[x])
        t = np.array(grouped_game.tags)
        if len(t) > 0:
            output_tags = [0] * len(tags_as_nums)
            for y in range(len(t)):
                output_tags[tags_as_nums[t[y]]] = 1
            game_names.append(grouped_game.name.unique()[0])
            game_ids_final.append(grouped_game.Game_ID.unique()[0])
            game_tags.append(output_tags)
            game_ratings.append(grouped_game.rating.unique()[0])
    
    final_data = {'game_name': game_names, 'game_id': game_ids_final, 'game_tags': game_tags, 'game_rating': game_ratings}
    df = pd.DataFrame(final_data)
    return df

def knn_fit_tags(data):
    data['game_tags'] = data['game_tags'].apply(lambda x: np.array(x))
    
    X = []
    for tag_list in np.array(data.game_tags):
        X.append(tag_list)
    y = np.array(data.game_name)

    knn = NearestNeighbors(5, 1.0, metric='cosine')
    knn.fit(X, y)
    return knn

# number_of_games must be <= 300
# filter: 'all', positive', 'mixed-positive', 'negative'
def get_games_from_tags(knn, data, game_data, game_id, filter='positive'):
    game_tags = data.loc[data['game_id'] == game_id].game_tags
    game_tags = np.array(game_tags)[0]

    _, name_indices = knn.kneighbors([game_tags], 400)

    name_indices = name_indices[0]
    random.shuffle(name_indices)
    

    grouped = game_data.groupby('Game_ID')

    game_names = []
    game_ids = []
    game_ratings = []
    game_tags = []
    for index in name_indices:
        game_names.append(data['game_name'][index])
        game_ids.append(data['game_id'][index])
        game_ratings.append(data['game_rating'][index])

        grouped_game = grouped.get_group(data['game_id'][index])
        game_tags.append(grouped_game.tags.unique())
    
    df = pd.DataFrame({'game_name': game_names, 'game_id': game_ids, 'game_rating': game_ratings, 'game_tags': game_tags})
    df.drop([df.loc[df['game_id'] == game_id].index[0]])
    
    if filter == 'positive':
        filters = ['Mostly Positive', 'Positive', 'Very Positive', 'Overwhelmingly Positive']
        df = df[df.game_rating.isin(filters)]
    elif filter == 'negative':
        filters = ['Mixed', 'Mostly Negative', 'Negative', 'Very Negative', 'Overwhelmingly Negative']
        df = df[df.game_rating.isin(filters)]
    elif filter == 'mixed-positive':
        filters = ['Mixed', 'Mostly Positive', 'Positive', 'Very Positive', 'Overwhelmingly Positive']
        df = df[df.game_rating.isin(filters)]
    
    return df