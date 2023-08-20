from mwrogue.esports_client import EsportsClient
from typing import Literal


class LeaguepediaClient:

    def __init__(self, wiki='lol'):
        self.wiki = wiki
        self.site = EsportsClient(wiki)

    def get_regions(self):
        """
        Returns a list of current regions
        """
        try:

            response = self.site.cargo_client.query(
                tables="Regions=R",
                fields="R.RegionLong, R.IsCurrent",
            )
        except:
            raise Exception("Error getting current regions")

        list_of_regions = [region['RegionLong'] for region in response]
        list_of_regions.append("International")
        # Since this is not a real region, we add it manually
        return list_of_regions

    def get_tournaments(self, region=None, date__gt=None, date__lt=None, year=None, name__contains=None):
        """
        Returns a list of tournaments
        :param region: Region of the tournament
        :param date__gt: Date greater than
        :param date__lt: Date less than
        :param year: Year of the tournament
        """
        response = None
        where_clauses = []

        if region is not None:
            where_clauses.append("T.Region='{}'".format(region))

        if date__gt is not None:
            where_clauses.append("T.Date>'{}'".format(date__gt))

        if date__lt is not None:
            where_clauses.append("T.Date<'{}'".format(date__lt))

        if year is not None:
            where_clauses.append("T.Date LIKE '%{}%'".format(year))

        if name__contains is not None:
            where_clauses.append("T.Name LIKE '%{}%'".format(name__contains))

        if where_clauses:
            where_clause = " AND ".join(where_clauses)
        else:
            where_clause = ""  # Empty WHERE clause to retrieve all data
        response = self.site.cargo_client.query(
            tables="Tournaments=T",
            fields="T.Name, T.Region, T.Date, T.OverviewPage",
            where=where_clause,
        )

        return response

    def manual_query(self, tables, join_on, fields, where):
        """
        Make a manual cargo query to the wiki
        :param tables: Tables to query
        :param fields: Fields to return
        :param where: Where clause
        """
        response = None

        response = self.site.cargo_client.query(
            tables=tables,
            join_on=join_on,
            fields=fields,
            where=where,
        )

        return response

    def get_games_from_tournament(self, overview_page):
        """
        Returns a list of games from a tournament
        :param tournament_name: Name of the tournament
        """
        response = None
        try:
            response = self.site.cargo_client.query(
                tables="MatchScheduleGame=MSG, MatchSchedule=MS",
                fields="RiotPlatformGameId, GameId, Blue, Red, Patch",
                where="MSG.OverviewPage='{}'".format(overview_page),
                join_on="MSG.MatchId=MS.MatchId",
                order_by="MS.DateTime_UTC ASC"
            )
        except:
            raise Exception("Error getting games from tournament")
        return response

    def get_champions(self):
        """
        Returns a list of champions
        """
        response = None

        try:
            response = self.site.cargo_client.query(
                tables="Champions=C",
                fields="C.Name, C.KeyInteger",
            )
        except:
            raise Exception("Error getting champions")

        return response

    def get_game_data_with_version(self,
                                   riot_platform_game_id: str,
                                   blue_team_name: str = None,
                                   red_team_name: str = None,
                                   version: int = 4):
        """
        Returns a dictionary with the game data
        :param riot_platform_game_id: Riot Platform Game id
        :version 4 or 5

        You must be sure that you are using the correct version. If you are not sure, use version 4.
        Otherwise, you can try with `get_game_data(riot_platform_game_id)`.
        """
        if version not in [4, 5]:
            raise ValueError("Version must be 4 or 5")

        response = None
        if riot_platform_game_id is None:
            raise Exception(
                "riot_platform_game_id cannot be None. This can be caused by a LPL game.")
        try:
            response = self.site.get_data_and_timeline(
                riot_platform_game_id, version)
        except:
            raise Exception("Error getting game data")

        # Assuming response[0] is a dictionary, you can add the blueTeam and redTeam keys here
        response[0]['blueTeam'] = blue_team_name
        response[0]['redTeam'] = red_team_name
        return response[0]

    def get_game_data(self, riot_platform_game_id: str,
                      blue_team_name: str = None,
                      red_team_name: str = None
                      ):
        """
        Returns a dictionary with the game data
        :param riot_platform_game_id: Riot Platform Game id

        This method will try with both of the versions of the API.
        It will first try with version 4, and if it fails, it will try with version 5.
        """
        try:
            # Try with version 4
            return self.get_game_data_with_version(
                riot_platform_game_id=riot_platform_game_id,
                blue_team_name=blue_team_name,
                red_team_name=red_team_name,
                version=4)
        except:
            # Try with version 5
            return self.get_game_data_with_version(
                riot_platform_game_id=riot_platform_game_id,
                blue_team_name=blue_team_name,
                red_team_name=red_team_name,
                version=5)
