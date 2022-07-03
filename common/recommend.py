from surprise import SVD, Reader, Dataset
from models.games import Game
from common.database import Database as db
import pandas as pd


class Recommend(object):
    def __init__(self):
        self.model = SVD(n_factors=80, lr_all=0.01, reg_all=0.04)
        reader = Reader(rating_scale=(1, 5))
        fetched_data = self.fetch_data()
        fetched_data = fetched_data.astype({"overall": int}, errors='raise')
        self.data = Dataset.load_from_df(fetched_data, reader)
        train_set = self.data.build_full_trainset()
        self.model.fit(train_set)

    def fetch_data(self) -> pd.DataFrame:
        ratings = db.find("ratings", {})
        rating_list = list(ratings)
        df = pd.DataFrame(rating_list)
        df_filtered = df[['reviewerID', 'asin', 'overall']]
        df_filtered = df_filtered[df_filtered.asin != '']
        return df_filtered

    def recommend(self, reviewerID, not_liked = False):
        df = self.fetch_data()
        asins = df[['asin']]
        asin_uniq = asins.drop_duplicates()

        predictions = []

        for index, row in asin_uniq.iterrows():
            prediction = self.model.predict(uid=reviewerID, iid=row['asin'])
            predictions.append(prediction)

        df_columns = pd.DataFrame(predictions, columns=['uid', 'iid', 'None', 'est', 'impossible'])
        df_columns = df_columns.drop(['None', 'impossible'], axis=1)

        if not_liked == True:
            df_columns = df_columns.sort_values(by='est', ascending=True)
        else:
            df_columns = df_columns.sort_values(by='est', ascending=False)

        already_rated = df[df['reviewerID'] == reviewerID]
        already_rated.columns = ['uid', 'iid', 'rating']
        condition = df_columns['iid'].isin(already_rated['iid'])
        df_columns.drop(df_columns[condition].index, inplace=True)
        return df_columns

    def recommend_user(self, reviewerID, n=15, not_liked=False):
        df = self.recommend(reviewerID=reviewerID, not_liked=not_liked)
        games = []
        for index, row in df.iterrows():
            game_in_row = None
            asin_value = row['iid']

            if len(games) > n:
                break

            try:
                game_in_row = Game.find_one_by('asin', row['iid'])
                if game_in_row is not None:
                    games.append(game_in_row)
            except:
                continue

        return games
