import React, { ReactNode, createContext, useState, useContext, useEffect} from 'react';
import { getTeams, getPlayers, predict } from './api.ts';


export interface Team {
  id: number;
  name: string;
  players: string[];
  rating: number;
}

export interface Player{
  id: number;
  name: string;
  rating: number;
}

export interface Prediction{
  team_A: string;
  team_B: string;
  win: number;
}

interface ContextProps {
  teams: Team[];
  players: Player[];
  predictions: Prediction[];
  handlePredict: (team1: string, team2: string) => void;
}


const Context = createContext<ContextProps | undefined>(undefined);

interface ContextProviderProps {
    children: ReactNode;
  }

export const ContextProvider: React.FC<ContextProviderProps> = ({ children }) => {

  const [teams, setTeams] = useState<Team[]>([]);
  const [players, setPlayers] = useState<Player[]>([]);
  const [predictions, setPredictions] = useState<Prediction[]>([]);

  useEffect(() => {
    carregarTimes();
    carregarPlayers();
  }, [])

  const carregarTimes = async () => {
    try {
      const teamsData = await getTeams();
      setTeams(teamsData);
    } catch (error) {
      console.error('Erro ao carregar times:', error);
    }
  };
  
  const carregarPlayers = async () => {
    try {
      const playersData = await getPlayers();
      setPlayers(playersData);
    } catch (error) {
      console.error('Erro ao carregar jogadores:', error);
    }
  };

  const handlePredict = async (team1: string, team2: string) => {
    try {
      const predictionData = await predict(team1, team2);
      setPredictions([...predictions, predictionData]);
      console.log(predictionData)
      console.log(team1, team2)
    } catch (error) {
      console.error('Erro ao prever:', error);
    }
  }


  return (
    <Context.Provider value={{ teams, players, predictions, handlePredict }}>
      {children}
    </Context.Provider>
  );
};

// eslint-disable-next-line react-refresh/only-export-components
export const useContexto = () => {
  const context = useContext(Context);
  if (!context) {
    throw new Error('useContexto deve ser usado dentro de um ContextProvider');
  }
  return context;
};