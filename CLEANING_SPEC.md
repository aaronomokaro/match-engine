# Cleaning Spec

Rules the cleaner applies to every season file. Each rule comes from

findings in `notebooks/01_explore.ipynb`.

## 1. Loading

- Read the header to get the expected number of columns.

- If a row has more values than the header, check the extras.

  - All empty: cut the row to the header length. (Finding 1)

  - Any contain data: stop with an error. Never drop real data silently.

- If the file fails to load with UTF-8, retry with latin-1 encoding.

- Drop rows where every value is empty.

## 2. Columns to keep

Select by name, never by position. (Finding 6)

| Source column | Output name | Meaning |

|---|---|---|

| Div | league | League code, e.g. E0 |

| Date | date | Match date |

| Time | time | Kick-off time (older seasons: empty) |

| HomeTeam | home_team | Home team |

| AwayTeam | away_team | Away team |

| FTHG | home_goals | Full-time home goals |

| FTAG | away_goals | Full-time away goals |

| FTR | result | H, D or A |

| B365H | odds_home | Bet365 home win odds |

| B365D | odds_draw | Bet365 draw odds |

| B365A | odds_away | Bet365 away win odds |

Also add a `season` column, e.g. "2003-04", taken from the file name.

- If any required column is missing (other than Time), stop with an error.

**[Decision] Why these:** results and teams for Elo, dates for ordering,

Bet365 odds for backtesting (Finding 10). Everything else is left out

until a later phase needs it. Adding columns later is easy; carrying

100+ unused ones makes every check harder.

## 3. Dates

- Try DD/MM/YY first, then DD/MM/YYYY. (Findings 2, 9)

- Apply per row, not per season. Don't assume which format a season uses.

- If a date matches neither, stop with an error.

- Check each parsed date falls between 1 July of the season's first

  year and 31 July of its second year.

## 4. Ordering

- Sort by date, then time, then home team name.

- Missing times sort after present times on the same date.

**[Decision] Why:** a team only plays once per day, so same-day order

doesn't change Elo. But sorting must give the same result every run,

or results aren't reproducible. Home team name is a tie-breaker that

always exists. (Finding 8)

## 5. Team names

- Strip leading and trailing spaces. (Finding 11)

- After combining all seasons, print every unique team name and review

  it by eye for duplicates like "Man United" vs "Manchester United".

## 6. Validation (run after cleaning)

- Each EPL season has 380 matches. Warn if not.

- No duplicate matches (same date, home team, away team).

- Goals are whole numbers, 0 or more.

- Result matches the goals: H if home > away, D if equal, A if less.

- Odds are greater than 1.0 where present.

- Report how many matches have missing Bet365 odds.  
