import AddMatchModal from "../../components/addMatchModal";
import React, { useState } from "react";
import { useContexto } from "../../context/context";
import { HomeStyled } from "./styles";

const Home: React.FC = () => {
    const [isOpen, setIsOpen] = useState<boolean>(false);
    const { teams, handlePredict, predictions } = useContexto();

    
    return (
        <HomeStyled>
            <h1>Previsão de Resultados de Valorant</h1>
            <div id="main">
                <div id="matches">
                    <button onClick={() => setIsOpen(true)}>Adicionar partida</button>
                    <AddMatchModal isOpen={isOpen} close={()=> setIsOpen(false)} handleSubmit={handlePredict} />
                    {predictions.map((prediction, index) => (
                        <div key={index}>
                            <h2>
                                <span style={{ color: prediction.win === 1 ? 'red' : 'green' }}>{prediction.team_A}</span>
                                 X 
                                 <span style={{ color: prediction.win === 1 ? 'green' : 'red' }}>{prediction.team_B}</span></h2>
                        </div>
                            ))}
                </div>
                <div id="ranking">
                    <h2>Ranking</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Time</th>
                                <th>Pontuação</th>
                            </tr>
                        </thead>
                        <tbody>
                            {teams.sort((a, b) => b.rating - a.rating).map((team, index) => index < 10 && (
                                <tr key={index}>
                                    <td>{team.name}</td>
                                    <td>{team.rating}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </HomeStyled>
    );
}

export default Home;