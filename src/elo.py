START_RATING = 1500
K = 20
HOME_ADVANTAGE = 60

def expected_score(home_rating, away_rating, home_advantage):
    gap = away_rating - (home_rating + home_advantage)
    return 1 / (1 + 10 ** (gap / 400))

if __name__ == "__main__":
    print(expected_score(1500, 1500, 0))
    print(expected_score(1550, 1450, 0))
    print(expected_score(1600, 1400, 0))
    print(expected_score(1500, 1500, HOME_ADVANTAGE))    