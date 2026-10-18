import pandas as pd

START_RATING = 1500
K = 20
HOME_ADVANTAGE = 60

def expected_score(home_rating, away_rating, home_advantage):
    gap = away_rating - (home_rating + home_advantage)
    return 1 / (1 + 10 ** (gap / 400))

def update_ratings(home_rating, away_rating, result, home_advantage, k):
    expected = expected_score(home_rating, away_rating, home_advantage)

    if result == "H":
        actual = 1
    elif result == "D":
        actual = 0.5
    else:
        actual = 0

    change = k * (actual - expected)
    return home_rating + change, away_rating - change


def add_elo(matches):
    if not matches["date"].is_monotonic_increasing:
        raise ValueError("Matches must be sorted by date before running Elo")

    ratings = {}
    elo_home = []
    elo_away = []
    season_end = {}
    current_season = None

    for home, away, result, season in zip(
        matches["home_team"], matches["away_team"], matches["result"], matches["season"]
    ):
        if season != current_season:
            if current_season is not None:
                season_end[current_season] = dict(ratings)
            current_season = season

        home_rating = ratings.get(home, START_RATING)
        away_rating = ratings.get(away, START_RATING)

        elo_home.append(home_rating)
        elo_away.append(away_rating)

        new_home, new_away = update_ratings(home_rating, away_rating, result, HOME_ADVANTAGE, K)
        ratings[home] = new_home
        ratings[away] = new_away

    season_end[current_season] = dict(ratings)

    matches = matches.copy()
    matches["elo_home"] = elo_home
    matches["elo_away"] = elo_away
    return matches, season_end

def find_promoted(matches):
    seasons = sorted(matches["season"].unique())

    teams = {}
    for season in seasons:
        teams[season] = set(matches.loc[matches["season"] == season, "home_team"])

    promoted = []
    for previous, current in zip(seasons, seasons[1:]):
        for team in sorted (teams[current] - teams[previous]):
            promoted.append((current, team))
    return promoted

def check_promoted(matches, promoted, first_n=10):
    matches = matches.copy()
    matches["expected_home"] = expected_score(matches["elo_home"], matches["elo_away"], HOME_ADVANTAGE)
    matches["actual_home"] = matches["result"].map({"H": 1, "D": 0.5, "A": 0})

    expected = []
    actual = []

    for season, team in promoted:
        games = matches[
            (matches["season"] == season)
            & ((matches["home_team"] == team) | (matches["away_team"] == team))
        ].head(first_n)

        for _, game in games.iterrows():
            if game["home_team"] == team:
                expected.append(game["expected_home"])
                actual.append(game["actual_home"])
            else:
                expected.append(1 - game["expected_home"])
                actual.append(1 - game["actual_home"])

    return sum(expected) / len(expected), sum(actual) / len(actual)

if __name__ == "__main__":
    matches = pd.read_csv("data/matches.csv", parse_dates=["date"])
    matches, season_end = add_elo(matches)

    for season, ratings in season_end.items():
        top = max(ratings, key=ratings.get)
        print(season, top, round(ratings[top]))   

    promoted = find_promoted(matches)
    print(len(promoted))
    print(promoted[:6]) 

    exp, act = check_promoted(matches, promoted)
    print(f"Promoted teams, first 10 matches: expected {exp:.3f}, actual {act:.3f}")       