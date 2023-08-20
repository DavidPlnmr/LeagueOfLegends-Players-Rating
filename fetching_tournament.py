# Author: David Paulino
# Date: 2023-08-06
# Usage : python fetching_tournament.py
# Dependencies: pandas, mwrogue
# Description : Get data from tournaments and save it to a csv file


from lib.stats_parser import StatsParser
from lib.leaguepedia_client import LeaguepediaClient
import pandas as pd


client = LeaguepediaClient()
stats_parser = StatsParser()


for region in client.get_regions():
    print(region)

region_selected = input("Choose a region and press enter: ")
year_selected = input("Choose a year and press enter (or skip): ")
name_contains = input("Enter a name and press enter (or skip): ")

# Replace year by None if empty
year_selected = year_selected if year_selected else None
# Replace name_contains by None if empty
name_contains = name_contains if name_contains else None

# You can change the call here to get the tournaments you want
tournaments = client.get_tournaments(region=region_selected,
                                     year=year_selected,
                                     name__contains=name_contains)

print("Tournaments: ")
for tournament in tournaments:
    print(tournament['OverviewPage'])

# Ask an input to the user
tournament_overview_page = input("Enter a tournament name : ")


# Get games from tournaments
games = client.get_games_from_tournament(tournament_overview_page)

print("Got {} games".format(len(games)))
print("-"*50)
df_games = pd.DataFrame(games)
print(df_games.head(10))
print("-"*50)

whole_data_games = []
count = 0
for game in games:
    # Get data from the game
    game_data = client.get_game_data(
        game["RiotPlatformGameId"], game["Blue"], game["Red"])

    participants_stats = stats_parser.get_participants_stats_from_game_any_version(
        game_data)
    # Add the data to the whole data
    whole_data_games.extend(participants_stats)
    count += 1
    print("Fetched {} games".format(count))


# Create a dataframe from the data
df = pd.DataFrame(whole_data_games)
print(df.shape)


# Find the name of the tournament based on the overview page
tournament_name = [
    tournament["Name"] for tournament in tournaments if tournament["OverviewPage"] == tournament_overview_page]
print(tournament_name)
file_name = tournament_name[0].replace(" ", "_")
# Save the data to a csv file
df.to_csv("data/" + file_name + ".csv", index=False)
