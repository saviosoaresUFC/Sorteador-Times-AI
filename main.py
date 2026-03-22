from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any
from our_ai_parser import extract_players
from sorter import draw_teams
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Sorteador de Times AI (Local)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DrawRequest(BaseModel):
    text: str
    num_teams: int

class DrawResponse(BaseModel):
    teams: List[List[Dict[str, Any]]]

@app.post("/api/sorteio", response_model=DrawResponse)
def sorteio_endpoint(request: DrawRequest):
    # AI Parser extrai os jogadores do texto bagunçado
    players = extract_players(request.text)
    
    # Sorteador distribui os jogadores em N times
    teams = draw_teams(players, request.num_teams)
    
    return DrawResponse(teams=teams)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8090, reload=True)
