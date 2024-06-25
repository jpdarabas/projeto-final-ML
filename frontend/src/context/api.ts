import axios from 'axios';

const API_URL = 'http://localhost:5000';

export const getTeams = async () => {
  try {
    const response = await axios.get(`${API_URL}/teams`);
    return response.data;
  } catch (error) {
    console.error('Erro no get de times:', error);
    throw error;
  }
};


export const getPlayers = async () => {
    try {
      const response = await axios.get(`${API_URL}/players`);
      return response.data;
    } catch (error) {
      console.error('Erro no get de players:', error);
      throw error;
    }
};

// No body passa um json com "team_A" e "team_B"
export const predict = async (team1: string, team2: string) => {
    try {
      const response = await axios.post(`${API_URL}/predict`, {team_A: team1, team_B: team2});
      return response.data;
    } catch (error) {
      console.error('Erro no post de predict:', error);
      throw error;
    }
}