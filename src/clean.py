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

def expected_result(row):
    if row["home_goals"] > row["away_goals"]:
        return "H"
    elif row["away_goals"] > row["home_goals"]:
        return "A"
    else:
        return "D"

def check_results(df):
    expected = df.apply(expected_result, axis=1)
    wrong = df[expected != df["result"]]
    if len(wrong) > 0:
        raise ValueError(f"Result doesn't match goals:\n{wrong}")

def goals_ok(row):
    for col in ["home_goals", "away_goals"]:
        g = row[col]
        if pd.isna(g):
            return False
        if g < 0:
            return False
        if g != int(g):
            return False
    return True

def check_goals(df):
    ok = df.apply(goals_ok, axis=1)
    bad = df[ok == False]
    if len(bad) > 0:
        raise ValueError(f"Invalid goals:\n{bad}")   
        
def check_duplicates(df):
    dupes = df.duplicated(subset=["home_team", "away_team"], keep=False)
    bad = df[dupes]
    if len(bad) > 0:
        raise ValueError(f"Duplicate matches:\n{bad}")

def odds_ok(row):
    for col in ["odds_home", "odds_draw", "odds_away"]:
        o = row[col]
        if pd.isna(o):
            continue
        if o <= 1:
            return False
    return True        

def check_odds(df):
    ok = df.apply(odds_ok, axis=1)
    bad = df[ok == False]
    if len(bad) > 0:
        raise ValueError(f"invalid odds:\n{bad}")

def check_match_count(df):
    season = df["season"].iloc[0]  
    if season in ["1993-94", "1994-95"]:
        expected = 462
    else:
        expected = 380
    if len(df) != expected:
        print(f"WARNING: {season} has {len(df)} matches, expected {expected}")   

def clean_season(path, name):
    df = load_raw(path)
    check_required(df)
    df = select_columns(df)
    df = parse_dates(df)
    df = clean_team_names(df)
    df = add_season(df, name)
    check_season_window(df)
    check_goals(df)
    check_results(df)
    check_duplicates(df)
    check_odds(df)
    check_match_count(df)
    return df

if __name__ == "__main__":
    for name in sorted(os.listdir("data/raw")):
        try:
            df = clean_season(f"data/raw/{name}", name)
            print(name, df.shape, "OK")  
        except Exception as e:
            print(name, "FAILED:", e)     
 

