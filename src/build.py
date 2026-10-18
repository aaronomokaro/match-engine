from curses import raw
import os
import pandas as pd
from clean import clean_season

def combine_all():
    combined = []
    for name in sorted(os.listdir("data/raw")):
        df = clean_season(f"data/raw/{name}", name)
        combined.append(df)
    all_matches = pd.concat(combined, ignore_index=True) 
    
    all_matches = all_matches.sort_values(
        ["date", "time", "home_team"],
    )
    all_matches = all_matches.reset_index(drop=True) 
    
    return all_matches

def save_matches(matches, path):
    tmp_path = f"{path}.tmp"
    matches.to_csv(tmp_path, index=False)
    os.replace(tmp_path, path)
    print(f"Saved {len(matches)} matches to {path}")

if __name__ == "__main__":
    matches = combine_all()
    save_matches(matches, "data/matches.csv")

    loaded = pd.read_csv("data/matches.csv", parse_dates=["date"])
    print(loaded.shape)
    print(loaded["date"].min(), loaded["date"].max())



        