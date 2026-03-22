import random
from typing import List, Dict, Any

def draw_teams(players: List[Dict[str, Any]], num_teams: int) -> List[List[Dict[str, Any]]]:
    if num_teams < 1:
        num_teams = 1
        
    teams = [[] for _ in range(num_teams)]
    
    goalkeepers = [p for p in players if p.get("is_goalkeeper")]
    field_players = [p for p in players if not p.get("is_goalkeeper")]
    
    # Embaralhar para garantir aleatoriedade
    random.shuffle(goalkeepers)
    random.shuffle(field_players)
    
    # Distribuir goleiros equitativamente
    for i, gk in enumerate(goalkeepers):
        team_index = i % num_teams
        teams[team_index].append(gk)
        
    # Distribuir jogadores de linha para equilibrar os tamanhos dos times
    for p in field_players:
        # Procurar o time que tem menos pessoas no momento
        smallest_team = min(teams, key=len)
        smallest_team.append(p)
        
    # Reordenar dentro de cada time (colocar goleiros primeiro)
    for team in teams:
        team.sort(key=lambda x: not x.get("is_goalkeeper"))
        
    return teams
