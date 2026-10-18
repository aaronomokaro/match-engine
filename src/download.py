import requests
import os
from datetime import date

def season_code(start_year):
    return  str(start_year)[-2:] + str(start_year + 1)[-2:]

def download_season(start_year):
    code = season_code(start_year)
    url = f"https://www.football-data.co.uk/mmz4281/{code}/E0.csv"
    path = f"data/raw/E0_{code}.csv"

    if os.path.exists(path) and start_year != current_season_start():
        print(f"Skipping {path} (already exists)")
        return


    response = requests.get(url, timeout=30)
    response.raise_for_status()

    tmp_path = f"{path}.tmp"
    with open(tmp_path, "wb") as f:
        f.write(response.content)

    os.replace(tmp_path, path)    
    print(f"saved {path}")   

def current_season_start():
    today = date.today()
    if today.month >= 8:
        return today.year
    else:
        return today.year - 1


for year in range(1993,current_season_start() + 1):
    try:
        download_season(year)
    except Exception as e:
        print(f"Failed {year}: {e}")    

                