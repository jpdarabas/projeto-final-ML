import { AddMatchModalStyled } from "./style";
import { useContexto, Team } from "../../context/context";
import { useState } from "react";
import Autocomplete from '@mui/material/Autocomplete';
import TextField from '@mui/material/TextField';

const AddMatchModal = ({ isOpen, close, handleSubmit }: { 
    isOpen: boolean; 
    close: () => void;
    handleSubmit: (team1: string, team2: string) => void; 
    }) => {
    const { teams } = useContexto();
    const [team1, setTeam1] = useState<Team | null>(null);
    const [team2, setTeam2] = useState<Team | null>(null);

    return (
        <AddMatchModalStyled
            isOpen={isOpen}
            onBackgroundClick={close}
            onEscapeKeydown={close}
        >
            <h1>Adicionar partida</h1>
            <div id='teamsContainer'>
                <div className="team">
                    <label htmlFor="Team1">Time 1</label>
                    <Autocomplete
                        id="team1"
                        options={teams}
                        getOptionLabel={(option) => option.name}
                        value={team1}
                        onChange={(_, newValue) => setTeam1(newValue)}
                        renderInput={(params) => <TextField {...params} label="Time 1" variant="outlined" />}
                    />
                    {/* <div className="playersContainer">
                        {team1 && team1.players.map(player => (
                            <div key={player}>
                                <TextField fullWidth name={player} defaultValue={player} variant="outlined" />
                            </div>
                        ))}
                    </div> */}
                </div>
                <div className="team">
                    <label htmlFor="Team2">Time 2</label>
                    <Autocomplete
                        id="team2"
                        options={teams}
                        getOptionLabel={(option) => option.name}
                        value={team2}
                        onChange={(_, newValue) => setTeam2(newValue)}
                        renderInput={(params) => <TextField {...params} label="Time 2" variant="outlined" />}
                    />
                    {/* <div className="playersContainer">
                        {team2 && team2.players.map(player => (
                            <div key={player}>
                                <TextField fullWidth name={player} defaultValue={player} variant="outlined" />
                            </div>
                        ))}
                    </div> */}
                </div>
            </div>
            <button id="add" onClick={()=>{
                handleSubmit(team1? team1.name: '', team2? team2.name: '');
                close();}}>Adicionar</button>
        </AddMatchModalStyled>
    );
}

export default AddMatchModal;
