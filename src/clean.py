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

def parse_dates(df):
    short = pd.to_datetime(df["date"], format="%d/%m/%y", errors="coerce")
    long = pd.to_datetime(df["date"], format="%d/%m/%Y", errors="coerce")
    parsed = short.fillna(long)

    bad = df.loc[parsed.isna(), "date"]
    if len(bad) > 0:
        raise ValueError(f"unrecognised dates:{list(bad)}")

    df["date"] = parsed    
    return df

def clean_team_names(df):
    df["home_team"] = df["home_team"].str.strip()
    df["away_team"] = df["away_team"].str.strip()
    return df

def season_label(name):
    code = name[3:7]
    first = int(code[:2])
    if first >= 90 :
        start = 1900 + first
    else:
        start = 2000 + first
    return f"{start}-{code[2:]}"

def add_season(df, name):
    df["season"] = season_label(name)
    return df   

def check_season_window(df):
    start_year = int(df["season"].iloc[0][:4])

    window_start = pd.Timestamp(start_year, 8, 1)
    window_end = pd.Timestamp(start_year + 1, 7, 31)

    outside = df[(df["date"] < window_start) | (df["date"] > window_end)]

    if len(outside) > 0:
        raise ValueError(f"Dates outside {window_start.date()} to {window_end.date()}:\n{outside}")

if __name__ == "__main__":
    for name in sorted(os.listdir("data/raw")):
        try:
            df = load_raw(f"data/raw/{name}")
            check_required(df)
            df = select_columns(df)
            df = parse_dates(df)
            df = clean_team_names(df)
            df = add_season(df, name)
            df.loc[0, "date"] = pd.Timestamp(2099, 1, 1)
            check_season_window(df)
            print(name, df.shape, "OK")  
        except Exception as e:
            print(name, "FAILED:", e)     
 

