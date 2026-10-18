import pandas as pd
import os

REQUIRED = {
    "Div": "league",
    "Date": "date",
    "HomeTeam": "home_team",
    "AwayTeam": "away_team",
    "FTHG": "home_goals",
    "FTAG": "away_goals",
    "FTR": "result",
}

OPTIONAL = {
    "Time": "time",
    "B365H": "odds_home",
    "B365D": "odds_draw",
    "B365A": "odds_away",
}

def fix_long_row(row, header_len):
    extras = row[header_len:]
    if any(v != "" for v in extras):
        raise ValueError(f" Extra values contain data: {extras}")
    return row[:header_len]    



def read_with_encoding(path, encoding):
    with open(path, encoding=encoding) as f:
        header_len = len(f.readline().split(","))

    df = pd.read_csv(
        path,
        encoding=encoding,
        engine="python",
        on_bad_lines=lambda row: fix_long_row(row, header_len)
    )

    df = df.dropna(how="all")    
    return df

def load_raw(path):
    try:
        return read_with_encoding(path, "utf-8")
    except UnicodeDecodeError:
        return read_with_encoding(path, "latin-1")        

def check_required(df):
    missing = []
    for col in REQUIRED:
        if col not in df.columns:
            missing.append(col)
    if missing:
            raise ValueError(f"missing required columns: {missing}") 

def select_columns(df): 
    for col in OPTIONAL:
        if col not in df.columns:
            df[col] = pd.NA

    
    columns = REQUIRED | OPTIONAL
    df = df[list(columns)]

    
    df = df.rename(columns=columns)
    return df

if __name__ == "__main__":
    for name in sorted(os.listdir("data/raw")):
        try:
            df = load_raw(f"data/raw/{name}")
            check_required(df)
            df = select_columns(df)
            print(name, list(df.columns))  
        except Exception as e:
            print(name, "FAILED:", e)     

   

