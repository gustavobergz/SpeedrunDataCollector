import csv
import os
from datetime import datetime, timedelta
import time
from tqdm import tqdm
import requests
from collections import defaultdict
import concurrent.futures
import logging
import random

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- CONFIGURAÇÕES CORRIGIDAS COM BASE NO LINK ---
GAME_ID = "y65797de"
CATEGORY_ID = "n2y350ed"                  # Categoria: No Coins (no hoverboard/no keys)

# Variável 1: Plataforma (Platform)
VAR_PLATFORM = "j84eeg2n"                  # ID da variável "Platform"
VAR_PLATFORM_VALUE = "21gy6p81"           # ID do valor para "Web" (extraído do link)

# Variável 2: Hoverboard
VAR_HOVERBOARD = "onv47omn"               # ID da variável "Hoverboard"
VAR_HOVERBOARD_VALUE = "81p9k88q"         # ID do valor para "No" (extraído do link)

# Datas para a coleta de dados
end_date = datetime.today()
start_date = datetime(2022, 1, 1)

# Nome do arquivo de saída
tsv_file = "data.tsv"

# Configuração de requests
SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json"
})
API_BASE = "https://www.speedrun.com/api/v1"

# Configurações de rate limiting
MAX_RETRIES = 5
BASE_DELAY = 1.0
MAX_WORKERS = 2

def handle_rate_limit(response, attempt ):
    if response.status_code in [420, 429]:
        retry_after = response.headers.get('Retry-After')
        wait_time = int(retry_after) if retry_after else (2 ** attempt) + random.uniform(1, 3)
        logger.warning(f"Rate limited. Waiting {wait_time:.1f} seconds...")
        time.sleep(wait_time)
        return True
    return False

def make_api_request(url, params, max_retries=MAX_RETRIES):
    for attempt in range(max_retries):
        try:
            time.sleep(BASE_DELAY + random.uniform(0.5, 1.5))
            response = SESSION.get(url, params=params, timeout=15)
            if handle_rate_limit(response, attempt):
                continue
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                logger.error(f"Failed after {max_retries} attempts: {e}")
                logger.error(f"Problematic URL: {e.request.url}")
                raise e
            wait_time = (2 ** attempt) + random.uniform(1, 3)
            logger.warning(f"Attempt {attempt + 1} failed. Waiting {wait_time:.1f}s: {e}")
            time.sleep(wait_time)
    return None

def process_day(current_day):
    data_str = current_day.strftime("%Y-%m-%d")
    url = f"{API_BASE}/leaderboards/{GAME_ID}/category/{CATEGORY_ID}"
    
    # --- PARÂMETROS CORRIGIDOS ---
    # Agora incluindo AMBOS os filtros com os IDs corretos do link
    params = {
        "top": 10,
        "embed": "players",
        f"var-{VAR_PLATFORM}": VAR_PLATFORM_VALUE,
        f"var-{VAR_HOVERBOARD}": VAR_HOVERBOARD_VALUE,
        "date": data_str
    }
    
    try:
        json_data = make_api_request(url, params)
        if not json_data or "data" not in json_data or "runs" not in json_data["data"]:
            logger.warning(f"No data for {data_str}")
            return data_str, None
        
        runs = json_data["data"]["runs"]
        players_data = {p["id"]: p["names"]["international"] for p in json_data["data"].get("players", {}).get("data", [])}
        day_data = {}
        
        for run in runs:
            try:
                time_s = run["run"]["times"]["primary_t"]
                run_id = run["run"]["id"]
                player_info = run["run"]["players"][0]
                player_name = players_data.get(player_info["id"]) if player_info["rel"] == "user" else player_info.get("name", f"Guest_{run_id[:8]}")
                
                if player_name not in day_data or time_s < day_data[player_name]:
                    day_data[player_name] = time_s
            except KeyError as e:
                logger.warning(f"Error processing run in {data_str}: {e}")
                continue
        
        logger.info(f"Processed {data_str}: {len(day_data)} players")
        return data_str, day_data
    except Exception as e:
        logger.error(f"Error processing {data_str}: {str(e)}")
        return data_str, None

def main():
    print(f"Iniciando coleta de dados de {start_date.strftime('%Y-%m-%d')} a {end_date.strftime('%Y-%m-%d')}")
    print(f"Categoria: No Coins (Web, No Hoverboard) | ID: {CATEGORY_ID}")
    
    daily_best_times = {}
    all_unique_players = set()
    dates_to_process = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
    
    with tqdm(total=len(dates_to_process), desc="Processing days") as pbar:
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_date = {executor.submit(process_day, date): date for date in dates_to_process}
            for future in concurrent.futures.as_completed(future_to_date):
                try:
                    data_str, day_data = future.result()
                    if day_data:
                        daily_best_times[data_str] = day_data
                        all_unique_players.update(day_data.keys())
                except Exception as e:
                    logger.error(f"Error with future: {e}")
                finally:
                    pbar.update(1)

    if not daily_best_times:
        logger.error("No data collected! Check logs for errors.")
        return
    
    print(f"\nProcessamento concluído. Dias com dados: {len(daily_best_times)}, Jogadores únicos: {len(all_unique_players)}")
    
    output_fieldnames = ["Dias"] + sorted(list(all_unique_players))
    
    with open(tsv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=output_fieldnames, delimiter='\t')
        writer.writeheader()
        for date_str in tqdm(sorted(daily_best_times.keys()), desc="Gerando TSV"):
            row = {"Dias": date_str, **{player: daily_best_times[date_str].get(player, 0) for player in output_fieldnames[1:]}}
            writer.writerow(row)
    
    print(f"✅ Arquivo {tsv_file} gerado com sucesso!")

if __name__ == "__main__":
    main()
