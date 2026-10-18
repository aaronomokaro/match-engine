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

if __name__ == "__main__":
    matches = pd.read_csv("data/matches.csv", parse_dates=["date"])
    matches, season_end = add_elo(matches)

    for season, ratings in season_end.items():
        top = max(ratings, key=ratings.get)
        print(season, top, round(ratings[top]))   