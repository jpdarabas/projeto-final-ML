from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
import pandas as pd


class AddRDFearure(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        RD_class = np.zeros(len(X))
        for i in range(len(X)):
          AR = X.iloc[i]['team_A_rating']
          BR = X.iloc[i]['team_B_rating']
          ARD = X.iloc[i]['team_A_RD']
          BRD = X.iloc[i]['team_B_RD']
          if (AR + ARD) > BR and (BR + BRD) > AR:
            RD_class[i] = 1
          elif (AR + ARD) > (BR - BRD) and (BR + BRD) > (AR - ARD):
            RD_class[i] = 2
          else:
            RD_class[i] = 3

          if AR > BR:
            RD_class[i] *= -1

        X['RD_class'] = RD_class
        return X

class AddChampionshipStats(BaseEstimator, TransformerMixin):
  def __init__(self, matches):
        self.matches = matches

  def fit(self, X, y=None):
    return self

  def transform(self, X):
    features_list = []
    cols = {j: i for i, j in enumerate(X.columns)}

    for row in X.values:
      wr_0_A, big_win_0_A, small_win_0_A, big_lose_0_A, small_lose_0_A, delta_rating_0_A = 0.5, 0.25, 0.25, 0.25, 0.25, 0
      wr_1_A, big_win_1_A, small_win_1_A, big_lose_1_A, small_lose_1_A, delta_rating_1_A = 0.5, 0.25, 0.25, 0.25, 0.25, 0
      wr_0_B, big_win_0_B, small_win_0_B, big_lose_0_B, small_lose_0_B, delta_rating_0_B = 0.5, 0.25, 0.25, 0.25, 0.25, 0
      wr_1_B, big_win_1_B, small_win_1_B, big_lose_1_B, small_lose_1_B, delta_rating_1_B = 0.5, 0.25, 0.25, 0.25, 0.25, 0

      tournaments_A = self.matches.loc[(self.matches['date'] < row[cols['date']])       &
                          ((self.matches['team_A'] == row[cols['team_A']])  |
                          (self.matches['team_B'] == row[cols['team_A']]))
                          ]['tournament']
      if len(tournaments_A) > 0:
        tournament_0_A = tournaments_A.iloc[-1]
        tournaments_1_A = tournaments_A.loc[tournaments_A != tournament_0_A]

        wr_0_A, big_win_0_A, small_win_0_A, big_lose_0_A, small_lose_0_A, delta_rating_0_A = self.__get_stats(tournament_0_A, row, cols, "team_A")

        if len(tournaments_1_A) > 0:
          tournament_1_A = tournaments_1_A.iloc[-1]
          wr_1_A, big_win_1_A, small_win_1_A, big_lose_1_A, small_lose_1_A, delta_rating_1_A = self.__get_stats(tournament_1_A, row, cols, "team_A")

      tournaments_B = self.matches.loc[(self.matches['date'] < row[cols['date']])       &
                          ((self.matches['team_A'] == row[cols['team_B']])  |
                          (self.matches['team_B'] == row[cols['team_B']]))
                          ]['tournament']

      if len(tournaments_B) > 0:
        tournament_0_B = tournaments_B.iloc[-1]
        tournaments_1_B = tournaments_B.loc[tournaments_B != tournament_0_B]
        wr_0_B, big_win_0_B, small_win_0_B, big_lose_0_B, small_lose_0_B, delta_rating_0_B = self.__get_stats(tournament_0_B, row, cols, "team_B")

        if len(tournaments_1_B) > 0:
          tournament_1_B = tournaments_1_B.iloc[-1]
          wr_1_B, big_win_1_B, small_win_1_B, big_lose_1_B, small_lose_1_B, delta_rating_1_B = self.__get_stats(tournament_1_B, row, cols, "team_B")

      features_list.append([wr_0_A, big_win_0_A,
                           small_win_0_A, big_lose_0_A,
                           small_lose_0_A, delta_rating_0_A,
                           wr_1_A, big_win_1_A,
                           small_win_1_A, big_lose_1_A,
                           small_lose_1_A, delta_rating_1_A,
                           wr_0_B, big_win_0_B,
                           small_win_0_B, big_lose_0_B,
                           small_lose_0_B, delta_rating_0_B,
                           wr_1_B, big_win_1_B,
                           small_win_1_B, big_lose_1_B,
                           small_lose_1_B, delta_rating_1_B]
                           )


    features_df = pd.DataFrame(features_list, columns=["team_A_tournament_wr",
                                                      "team_A_tournament_big_win_ratio",
                                                      "team_A_tournament_small_win_ratio",
                                                      "team_A_tournament_big_lose_ratio",
                                                      "team_A_tournament_small_lose_ratio",
                                                      "team_A_tournament_delta_rating",
                                                      "team_A_last_tournament_wr",
                                                      "team_A_last_tournament_big_win_ratio",
                                                      "team_A_last_tournament_small_win_ratio",
                                                      "team_A_last_tournament_big_lose_ratio",
                                                      "team_A_last_tournament_small_lose_ratio",
                                                      "team_A_last_tournament_delta_rating",
                                                      "team_B_tournament_wr",
                                                      "team_B_tournament_big_win_ratio",
                                                      "team_B_tournament_small_win_ratio",
                                                      "team_B_tournament_big_lose_ratio",
                                                      "team_B_tournament_small_lose_ratio",
                                                      "team_B_tournament_delta_rating",
                                                      "team_B_last_tournament_wr",
                                                      "team_B_last_tournament_big_win_ratio",
                                                      "team_B_last_tournament_small_win_ratio",
                                                      "team_B_last_tournament_big_lose_ratio",
                                                      "team_B_last_tournament_small_lose_ratio",
                                                      "team_B_last_tournament_delta_rating",])



    X[features_df.columns] = features_df
    return X

  def __get_stats(self, tournament, row, cols, team):
    X_t = self.matches.loc[((self.matches['date'] < row[cols['date']])       &
                ((self.matches['team_A'] == row[cols[team]])  |
                (self.matches['team_B'] == row[cols[team]]))) &
                  (self.matches['tournament'] == tournament)
                ]
    X_t = X_t.copy()
    X_t['win'] = np.where(X_t['team_A'] == row[cols[team]], 1 - X_t['win'], X_t['win'])
    X_t['rating'] = np.where(X_t['team_A'] == row[cols[team]], X_t['team_A_rating'], X_t['team_B_rating'])

    wr = X_t['win'].mean()
    if len(X_t) == 0:
      print(tournament, row[cols[team]])
    big_win = len(X_t.loc[(X_t['win'] == 1) &
                      ((X_t['A_score'] == 0)      |
                        (X_t['B_score'] == 0))
                      ]) / len(X_t)
    small_win = wr - big_win

    big_lose = len(X_t.loc[(X_t['win'] == 0) &
                      ((X_t['A_score'] == 0)      |
                        (X_t['B_score'] == 0))
                      ]) / len(X_t)

    small_lose = 1 - wr - big_lose

    delta_rating = X_t.iloc[-1]['rating'] - X_t.iloc[0]['rating']
    return wr, big_win, small_win, big_lose, small_lose, delta_rating

class AddDiff(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        rating_diff = X['team_B_rating'] - X['team_A_rating']

        team_B_avg_rating = X[['team_B_player_1_rating',
                             'team_B_player_2_rating',
                             'team_B_player_3_rating',
                             'team_B_player_4_rating',
                             'team_B_player_5_rating']].mean(axis=1)

        team_A_avg_rating = X[['team_A_player_1_rating',
                                'team_A_player_2_rating',
                                'team_A_player_3_rating',
                                'team_A_player_4_rating',
                                'team_A_player_5_rating']].mean(axis=1)

        player_rating_diff = team_B_avg_rating - team_A_avg_rating

        X[['rating_diff', 'player_rating_diff']] = np.column_stack((rating_diff, player_rating_diff))
        return X
