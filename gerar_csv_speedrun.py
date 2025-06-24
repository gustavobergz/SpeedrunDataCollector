import requests
import csv
from datetime import datetime, timedelta
import time
from tqdm import tqdm

# Configuração da API
GAME_ID = "y65797de"
CATEGORY_ID = "n2y350ed"
VAR_PLATFORM = "j84eeg2n"
VAR_PLATFORM_VALUE = "21gy6p81"  # Mobile
VAR_HOVERBOARD = "onv47omn"
VAR_HOVERBOARD_VALUE = "p127j34q"  # No Coins, No Hoverboard, No Keys

# Datas
start_date = datetime(2022, 1, 1)
end_date = datetime.today()
csv_file = "data.csv"

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "Mozilla/5.0"})
API_BASE = "https://www.speedrun.com/api/v1"

daily_best_times = {}
all_unique_players = set()

total_days = (end_date - start_date).days + 1
pbar = tqdm(total=total_days, desc="Baixando dados")

current_day = start_date

while current_day <= end_date:
    date_str = current_day.strftime("%Y-%m-%d")
    url = f"{API_BASE}/leaderboards/{GAME_ID}/category/{CATEGORY_ID}"
    params = {
        "top": 10,
        "embed": "players",
        f"var-{VAR_PLATFORM}": VAR_PLATFORM_VALUE,
        f"var-{VAR_HOVERBOARD}": VAR_HOVERBOARD_VALUE,
        "date": date_str
    }

    max_attempts = 3
    success = False
    for attempt in range(max_attempts):
        try:
            response = SESSION.get(url, params=params, timeout=30)
            response.raise_for_status()
            success = True
            break
        except requests.exceptions.ReadTimeout:
            print(f"⏳ Timeout em {date_str}, tentativa {attempt + 1}/{max_attempts}")
            time.sleep(3 * (attempt + 1))
        except Exception as e:
            print(f"⚠️ Erro em {date_str}: {e}")
            break

    if not success:
        print(f"❌ Falha definitiva em {date_str}. Pulando.")
        current_day += timedelta(days=1)
        pbar.update(1)
        continue

    json_data = response.json()
    runs = json_data.get("data", {}).get("runs", [])

    # 🔒 Correção robusta para evitar KeyError
    players_data = {}
    for p in json_data["data"].get("players", {}).get("data", []):
        player_id = p.get("id")
        player_name = p.get("names", {}).get("international", "Unknown")
        if player_id:
            players_data[player_id] = player_name

    daily_best_times.setdefault(date_str, {})

    for run in runs:
        time_s = run["run"]["times"]["primary_t"]
        run_id = run["run"]["id"]
        player_info = run["run"]["players"][0]

        if player_info["rel"] == "user":
            player_id = player_info["id"]
            player_name = players_data.get(player_id, f"User_{player_id[:6]}")
        else:
            player_name = player_info.get("name", "Guest")
            if player_name == "Guest":
                player_name += "_" + run_id[:6]

        all_unique_players.add(player_name)
        current_best = daily_best_times[date_str].get(player_name, float("inf"))
        daily_best_times[date_str][player_name] = min(current_best, time_s)

    current_day += timedelta(days=1)
    pbar.update(1)
    time.sleep(0.5)  # respeita a API

pbar.close()

# Exportar como CSV
fieldnames = ["Dias"] + sorted(all_unique_players)
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=",")
    writer.writeheader()

    for date in sorted(daily_best_times):
        row = {"Dias": date}
        for player in fieldnames[1:]:
            row[player] = daily_best_times[date].get(player, 0)
        writer.writerow(row)

print(f"\n✅ Arquivo CSV gerado com sucesso: {csv_file}")
