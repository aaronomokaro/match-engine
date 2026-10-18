## Using conda instead of venv

Decision: Use a conda environment with Python 3.12.

Why: My Mac's built-in Python is 3.9, which is too old for
scikit-learn. venv can only use a Python that's already
installed, so it would have been stuck on 3.9. The
alternative was installing Python 3.12 separately, then using
venv. Conda was already installed and can provide Python 3.12
itself, so it was the simpler route.

Downside: Anyone else running this project needs Anaconda,
or has to install Python 3.12 themselves and use venv.

## Not storing the data folder in git

Decision: Exclude data/ from git using .gitignore.

Why: The data can be rebuilt at any time by running the
pipeline, which downloads it from football-data.co.uk. Git
is built for tracking code, and storing every version of
the CSVs would bloat the repository. The data also belongs
to football-data.co.uk, so it isn't mine to redistribute.

Downside: Reproducibility depends on football-data.co.uk.
If the site goes offline, anyone cloning the repo can't get
the data. If the site edits an old file, they'd get
different data and different results from mine without
knowing why.

## Using Bet365 odds for backtesting

Decision: Use Bet365 home/draw/away odds (B365H, B365D, B365A).

Why: Bet365 is the only bookmaker checked that is present and complete
in all three sampled seasons (2003/04, 2012/13, 2025/26). Pinnacle,
usually the sharpest benchmark, is missing for 170 of 380 matches in
2025/26.

Downside: Results only measure performance against one bookmaker. Other
bookmakers may offer better odds on some matches, and Bet365 is not the
sharpest market, so an edge against Bet365 is not proof of an edge
against the market as a whole. Only 3 of 20+ seasons were checked.: