from download import download_all
from build import combine_all, save_matches


def run():
    download_all()
    matches = combine_all()
    save_matches(matches, "data/matches.csv")


if __name__ == "__main__":
    run()