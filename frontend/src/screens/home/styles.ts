import styled from "styled-components";

export const HomeStyled = styled.div`
    align-items: center;
    justify-content: center;
    margin-top: 50px;
    flex-direction: row;

    & #main{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 40px;
    }

    & #matches{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    & #ranking{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    & span{
        margin-left: 2vw;
        margin-right: 2vw;

    }

`