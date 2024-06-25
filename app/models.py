import pandas as pd
from app.transformers import AddRDFearure, AddDiff, AddChampionshipStats
from sklearn.pipeline import Pipeline
import pickle
from datetime import datetime

features = ['best_of', 'tier', 'RD_class', 'team_A_tournament_wr',
       'team_A_tournament_big_win_ratio', 'team_A_tournament_small_win_ratio',
       'team_A_tournament_big_lose_ratio',
       'team_A_tournament_small_lose_ratio', 'team_A_tournament_delta_rating',
       'team_A_last_tournament_wr', 'team_A_last_tournament_big_win_ratio',
       'team_A_last_tournament_small_win_ratio',
       'team_A_last_tournament_big_lose_ratio',
       'team_A_last_tournament_small_lose_ratio',
       'team_A_last_tournament_delta_rating', 'team_B_tournament_wr',
       'team_B_tournament_big_win_ratio', 'team_B_tournament_small_win_ratio',
       'team_B_tournament_big_lose_ratio',
       'team_B_tournament_small_lose_ratio', 'team_B_tournament_delta_rating',
       'team_B_last_tournament_wr', 'team_B_last_tournament_big_win_ratio',
       'team_B_last_tournament_small_win_ratio',
       'team_B_last_tournament_big_lose_ratio',
       'team_B_last_tournament_small_lose_ratio',
       'team_B_last_tournament_delta_rating', 'rating_diff',
       'player_rating_diff']


teams = pd.read_parquet('app/datasets/teams.parquet')
teams24 = pd.read_parquet('app/datasets/teams24.parquet')
players = pd.read_parquet('app/datasets/players.parquet')
matches = pd.read_parquet('app/datasets/matches.parquet')


pipeline = Pipeline([
        ('AddRDFearure', AddRDFearure()),
        ('AddChampionshipStats', AddChampionshipStats(matches=matches)),
        ('AddDiff', AddDiff()),
        ])

class Prediction:
    def __init__(self, team_A: str, team_B: str, best_of: int = 3):
        self.df = pd.DataFrame({
            "date": [datetime.now().strftime('%Y-%m-%d')],
            "best_of": [best_of],
            "team_A": [team_A],
            "team_B": [team_B],
            })
        self.team_A = teams.loc[teams['name'] == team_A].iloc[0]
        self.team_B = teams.loc[teams['name'] == team_B].iloc[0]
        self.df["tier"] = matches.loc[(matches["team_A"] == team_A) |
                                (matches["team_A"] == team_B) |
                                (matches["team_B"] == team_A) |
                                (matches["team_B"] == team_B) ].iloc[-1]['tier']
        self.df["tournament"] = matches.loc[(matches["team_A"] == team_A) |
                                (matches["team_A"] == team_B) |
                                (matches["team_B"] == team_A) |
                                (matches["team_B"] == team_B) ].iloc[-1]['tournament']

        self.df["team_A_rating"] = self.team_A["rating"]
        self.df["team_B_rating"] = self.team_B["rating"]

        self.df["team_A_RD"] = self.team_A["RD"]
        self.df["team_B_RD"] = self.team_B["RD"]

        for i in range(5):
            self.df[f"team_A_player_{i+1}"] = self.team_A["players"][i]
            self.df[f"team_B_player_{i+1}"] = self.team_B["players"][i]

            self.df[f"team_A_player_{i+1}_rating"] = players.loc[players["name"] == self.team_A["players"][i]]["rating"].iloc[0]
            self.df[f"team_B_player_{i+1}_rating"] = players.loc[players["name"] == self.team_B["players"][i]]["rating"].iloc[0]

            self.df[f"team_A_player_{i+1}_RD"] = players.loc[players["name"] == self.team_A["players"][i]]["RD"].iloc[0]
            self.df[f"team_B_player_{i+1}_RD"] = players.loc[players["name"] == self.team_B["players"][i]]["RD"].iloc[0]

        self.df = pipeline.fit_transform(self.df)
        
        self.X = self.df[features].copy()

        with open('app/datasets/encoder.pkl', 'rb') as e:
            encoder = pickle.load(e)
        self.X["tier"] = encoder.transform(self.X[["tier"]])

        numeric_features = self.X.select_dtypes(include=['int64', 'float64']).columns

        with open('app/datasets/scaler.pkl', 'rb') as s:
            scaler = pickle.load(s)

        self.X[numeric_features] = scaler.transform(self.X[numeric_features])

        with open('app/datasets/model.pkl', 'rb') as f:
            self.model = pickle.load(f)

        self.prediction = self.predict()
    def predict(self):
        return self.model.predict(self.X)
