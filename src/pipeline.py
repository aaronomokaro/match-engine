from download import download_all
from build import combine_all, save_matches
from elo import add_elo


def run():
    download_all()

    matches = combine_all()
    save_matches(matches, "data/matches.csv")

    matches_elo, _ = add_elo(matches)
    save_matches(matches_elo, "data/matches_elo.csv")


if __name__ == "__main__":
    run()