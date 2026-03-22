import re
import unidecode

def clean_text(text: str) -> str:
    return unidecode.unidecode(text).lower()

def is_goalkeeper(line: str) -> bool:
    cleaned = clean_text(line)
    keywords = ["goleiro", "gol", "gly", "arqueiro", "paredao", "gk"]
    for kw in keywords:
        if re.search(r"\b" + kw + r"\b", cleaned):
            return True
    return False

def extract_players(raw_text: str):
    players = []
    lines = raw_text.split('\n')
    
    # Encontrar o início real da lista (primeiro item número 1) para ignorar cabeçalhos soltos
    start_idx = 0
    for i, line in enumerate(lines):
        if re.match(r"^\s*1[.\-\)]+\s*\w", line.strip()):
            start_idx = i
            break
            
    if start_idx > 0:
        lines = lines[start_idx:]
    
    in_suplentes = False
    in_goleiros = False
    
    lixo_regex = r"(?i)\b(pago|pix|pg|pendente|confirmado|ok|transferencia|dinheiro|cpf|cnpj|sim)\b"
    dinheiro_regex = r"(?i)(r\$\s*[\d\,\.]+|[\d\,\.]+\s*reais)"
    
    for line in lines:
        original_line = line.strip()
        if not original_line:
            continue
            
        line_clean = clean_text(original_line)
        
        # Mudanças de seção
        if "suplente" in line_clean or "espera" in line_clean:
            in_suplentes = True
            in_goleiros = False
            continue
        # Algumas vezes colocam "Goleiros:\n1. Nome", ou "Goleiros: Nome1, Nome2"
        if "goleiro" in line_clean and ":" in line_clean:
            in_goleiros = True
            in_suplentes = False
            continue
        if "linha" in line_clean and ":" in line_clean:
            in_goleiros = False
            in_suplentes = False
            continue
            
        if in_suplentes:
            continue
            
        # Pular cabeçalhos inúteis
        if re.search(r"horario|horário|valor|lista de|baba dos|pix[:\s]|chave", line_clean):
            continue
        if "@" in original_line:
            continue
            
        match = re.match(r"^(\d+)[.\-°º\]\)]*\s*(.*)$", original_line)
        match_dash = re.match(r"^[\-\*]\s*(.*)$", original_line)
        
        if match:
            name_part = match.group(2)
        elif match_dash:
            name_part = match_dash.group(1)
        else:
            if len(original_line.split()) > 4:
                continue
            name_part = original_line
            
        goalkeeper = True if in_goleiros else is_goalkeeper(name_part)
        
        # Limpezas prévias antes de remover pontuação
        name_part = re.sub(r"\([^\)]*\)", "", name_part)
        name_part = re.sub(r"\[[^\]]*\]", "", name_part)
        name_part = re.sub(r"\{[^\}]*\}", "", name_part)
        
        name_part = re.sub(dinheiro_regex, " ", name_part)
        name_part = re.sub(lixo_regex, " ", name_part)
        name_part = re.sub(r"(?i)\b(goleiro|gol|gly|arqueiro|gk)\b", " ", name_part)
        
        # Manter letras, números, espaços e alguns acentos comuns (À-ÿ)
        name_part = re.sub(r"[^\w\sÀ-ÿ]", " ", name_part)
        
        name_part = re.sub(r"\b\d+\b", " ", name_part)
        
        final_name = " ".join(name_part.split()).strip()
        
        if len(final_name) > 1:
            players.append({
                "name": final_name.title(),
                "is_goalkeeper": goalkeeper
            })

    return players
