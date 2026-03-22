# Sorteador de Times com Inteligência Artificial Local

Uma API de alto desempenho construída em **FastAPI** e **Python**. O objetivo é receber listas de jogadores de futebol – frequentemente bagunçadas, oriundas do WhatsApp, contendo chaves PIX, informações de pagamento, lixos visuais, horários e suplentes – e limpar tudo isso para gerar um sorteio justo e dividido em equipes.

O diferencial deste projeto é utilizar um **Parser Heurístico Inteligente** (rodando 100% localmente) em vez de APIs externas de LLM, o que garante máxima velocidade e zero custo com inteligência artificial.

## 🚀 Funcionalidades

- **API Veloz**: Servida via FastAPI com validação de dados usando Pydantic.
- **Parser Resiliente**: Utiliza heurísticas avançadas e Expressões Regulares (Regex) para ignorar cabeçalhos, encontrar padrões de listas (ex: `1. Nome`, `- Nome`), filtrar valores (ex: `R$ 10,00`) e remover gírias comuns ("pago", "pix", "ok", "confirmado").
- **Identificação de Goleiros**: Reconhece automaticamente quem é goleiro a partir de palavras próximas ao nome ou quando organizados em uma subseção "Goleiros:".
- **Algoritmo de Sorteio**: Embaralha jogadores e goleiros separadamente para distribuir os goleiros uniformemente por todos os times, colocando o restante da equipe sempre no time mais vazio.

## 💻 Instalação e Uso

1. Clone o repositório para a sua máquina:
   ```bash
   git clone https://github.com/SEU_USUARIO/sorteador-times-ai.git
   cd sorteador-times-ai
   ```

2. Crie e ative um ambiente virtual (VENV):
   ```bash
   python -m venv venv
   
   # No Windows:
   .\venv\Scripts\activate
   
   # No Linux/Mac:
   source venv/bin/activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Suba o servidor:
   ```bash
   uvicorn main:app --reload --port 8090
   ou
   .\venv\Scripts\uvicorn.exe main:app --port 8090
   ```

5. Acesse e teste a API pela interface Swagger UI interativa:
   **[http://localhost:8090/docs](http://localhost:8090/docs)**

## ⚽ Exemplo de Payload (POST `/api/sorteio`)

```json
{
  "text": "Lista do racha 20/03\nSexta-feira\nHorário: 20\nPix: nomeparateste@alu.ufc.br\nValor 8,4\n\n1. Veríssimo✅\n2. Warley\n3. Altino✅\n4. Dourado\n\nGoleiros:\n1. Ramiro",
  "num_teams": 2
}
```

O sistema devolverá um JSON contendo a divisão limpa e perfeitamente equilibrada das equipes!
