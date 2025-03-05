# Author: David Paulino
# Date: 2023-08-06
# Usage : python fetching_multiple_tournaments.py
# Note : You can change the values of tournament_names and years to get the tournaments you want
# Dependencies: pandas, mwrogue
# Description : Get data from tournaments and save it to a csv file


from lib.stats_parser import StatsParser
from lib.leaguepedia_client import LeaguepediaClient
from concurrent.futures import ThreadPoolExecutor
import pandas as pd

client = LeaguepediaClient()
stats_parser = StatsParser()
tournament_names = ["LFL 20%%", "LCK 20%%", "LEC 20%%"]
years = ["2025"]


def process_tournament(tournament):
    games_data_from_tournament = []
    games = client.get_games_from_tournament(tournament['OverviewPage'])
    for game in games:

        game_data = client.get_game_data(
            game["RiotPlatformGameId"], game["Blue"], game["Red"])
        participants_stats = stats_parser.get_participants_stats_from_game_any_version(
            game_data)
        games_data_from_tournament.extend(participants_stats)

    df = pd.DataFrame(games_data_from_tournament)
    df.to_csv("data/{}.csv".format(tournament['Name'].replace(" ", "_")))
    print("Saved data for tournament {}".format(tournament['Name']))


# You can adjust max_workers as needed
with ThreadPoolExecutor(max_workers=8) as executor:
    tournaments = []
    for tournament_name in tournament_names:
        # Fetching the name of the tournament

        for year in years:
            print("Fetching {} {}".format(tournament_name.split(" ")[0], year))
            tournaments.extend(client.get_tournaments(
                name__contains=tournament_name, year=year))

    print("Got {} tournaments".format(len(tournaments)))
    executor.map(process_tournament, tournaments)

print("Done")
