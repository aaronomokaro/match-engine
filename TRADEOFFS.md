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
against the market as a whole. Only 3 of 20+ seasons were checked.

## Re-downloading the current season every run

Decision: Skip finished seasons that already exist, but always
re-download the current season.

Why: football-data.co.uk updates the current season's file as matches
are played. Skipping it once it exists would freeze it at an old
version, with no error to warn me.

Downside: One extra download on every run, even if nothing changed.
If the site's file is briefly broken or incomplete when I download
it, that version replaces my last good copy.

## Keeping seasons without odds

Decision: Keep all seasons from 1993/94, even though Bet365 odds only
exist from 2002/03.

Why: Elo starts every team at 1500 and needs many matches to learn real
strengths. The earlier seasons act as a warm-up, so ratings are sensible
by the time the backtest starts in 2002/03.

Downside: The backtest covers fewer seasons than the full dataset.
Football in the 1990s may differ from today, so early results could
pull ratings in ways that matter less now.

## Season window: 1 August to 31 July

Decision: A match's date must fall between 1 August of its season's
first year and 31 July of its second year.

Why: Every season in the data fits (earliest start 5 Aug, latest end
26 Jul in the COVID season). Windows touch end to end, so every date
belongs to exactly one season, unlike a 1 July start, which overlapped
the next season by a month.

Downside: If a future season ever starts in July, every match before
1 August would fail validation. The rule would need changing.