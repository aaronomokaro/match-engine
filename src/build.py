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
    return all_matches

if __name__ == "__main__":
    matches = combine_all()
    print(matches.shape)


        