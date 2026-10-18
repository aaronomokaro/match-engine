def season_code(start_year):
    return  str(start_year)[-2:] + str(start_year + 1)[-2:]

print(season_code(2003))
print(season_code(1999))
print(season_code(2025))
