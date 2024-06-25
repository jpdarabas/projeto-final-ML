from flask import Flask, jsonify, request
from flask_cors import CORS
from app.models import teams, players, Prediction, teams24


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

    @app.route('/teams', methods=['GET'])
    def getTeams():
        return jsonify(teams24.drop(columns="players").to_dict(orient="records"))
    
    @app.route('/players', methods=['GET'])
    def getPlayers():
        return jsonify(players.to_dict(orient="records"))
    
    @app.route('/predict', methods=['POST'])
    def predict():
        data = request.get_json()
        
        team_A = data['team_A']
        team_B = data['team_B']

        prediction = Prediction(team_A, team_B)
        predict = {
            'team_A': team_A,
            'team_B': team_B,
            'win': int(prediction.prediction[0])
        }

        return jsonify(predict)


    @app.route('/update-team-a', methods=['PATCH'])
    def updateTeamA():
        data = request.get_json()
        team_A = data['team_A']
        team_A = teams.query(f'name == {team_A}').iloc[0]
        return jsonify(team_A.to_dict())

    return app
