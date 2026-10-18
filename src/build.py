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



if __name__ == "__main__":
    matches = combine_all()

    teams = sorted(set(matches["home_team"]) | set(matches["away_team"]))
    print(len(teams))
    for team in teams:
        print(team)


        