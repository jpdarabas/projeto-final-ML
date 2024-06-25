# Previsão de resultado de partidas de Valorant utilizando técnicas de Machine Learning

### Endpoints da API:

* [GET] /teams
  > Retorna os times
  
* [GET] /players
  > Retorna os jogadores
  
* [POST] /predict
  > body (JSON)
  ```JSON
  {
    "team_A": "time A",
    "team_B": "time B"
  }
  ```
  > retorna:
  ```JSON
  {
    "predict": "0" // para vitória do time A
  }
  ```
   ```JSON
  {
    "predict": "1" // para vitória do time B
  }
  ```
