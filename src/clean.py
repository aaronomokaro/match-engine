import pandas as pd
import os

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


for name in sorted(os.listdir("data/raw")):
    try:
        df = load_raw(f"data/raw/{name}")
        print(name, df.shape)
    except Exception as e:
        print(name, "FAILED:", e)        

