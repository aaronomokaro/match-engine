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


print(update_ratings(1600, 1400, "A", 0, 20))
print(update_ratings(1550, 1450, "D", 0, 20))
print(update_ratings(1500, 1500, "D", 0, 20))    