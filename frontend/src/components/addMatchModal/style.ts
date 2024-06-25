import Modal from 'styled-react-modal'

export const AddMatchModalStyled = Modal.styled`
    width: 512px;
    height: auto;
    background-color: #f2f2f2;
    border-radius: 10px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.15);
    padding: 20px;

    & h1 {
        color: #333;
        font-size: 24px;
        margin-bottom: 20px;
    }

    & .playersContainer{
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }   

    & .playersContainer div{
        width: 100%;
    }   

    & #teamsContainer{
        display: flex;
        flex-direction: row;
        gap: 20px;
    }

    & .team{
        width: 100%;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    & #add{
        background-color: #333;
        color: #fff;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        margin-top: 20px;
    }
`
