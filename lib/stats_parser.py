from lib.leaguepedia_client import LeaguepediaClient


class StatsParser:

    def __init__(self):
        self.client = LeaguepediaClient()
        self.champions = self.client.get_champions()

    def extract_stats_from_participant(self, stats_from_participant):
        # First let's extract the stats from the participant
        stats_extracted = {}
        for key, value in stats_from_participant.items():

            if isinstance(value, dict):
                for key2, value2 in value.items():
                    stats_extracted[key2] = value2
            else:
                stats_extracted[key] = value

        return stats_extracted

    def get_participants_stats_from_game_v4(self, game_json):
        """
        This method only works with the v4 version of the API
        """
        participants = game_json["participants"]
        participants_data = []
        participantIdentities = game_json["participantIdentities"]
        role_indices = {0: "TOP", 1: "JUNGLE",
                        2: "MID", 3: "ADC", 4: "SUPPORT"}

        for i, participant in enumerate(participants):
            participant_id = participant["participantId"]
            summoner_name = next((p["player"]["summonerName"]
                                  for p in participantIdentities if p["participantId"] == participant_id), None)
            championName = next(
                (c["Name"] for c in self.champions if c["KeyInteger"] is not None and int(participant["championId"]) == int(c["KeyInteger"])), None)

            role = role_indices[i % 5]  # Cycle through roles using modulo
            stats = self.extract_stats_from_participant(participant["stats"])

            participants_data.append({
                "gameId": game_json["gameId"],
                "participantId": participant["participantId"],
                "summonerName": summoner_name,
                "championId": participant["championId"],
                "championName": championName,
                "teamId": participant["teamId"],
                "blueTeam": game_json["blueTeam"],
                "redTeam": game_json["redTeam"],
                "role": role,
                # Get only the chars before the second dot
                "patch": '.'.join(game_json["gameVersion"].split(".")[0:2]),
                **stats
            })

        return participants_data

    def get_participants_stats_from_game_v5(self, game_json):
        patch = '.'.join(game_json["gameVersion"].split(".")[0:2])
        gameId = game_json["gameId"]
        participants = game_json["participants"]

        participants_data = []
        role_indices = {0: "TOP", 1: "JUNGLE",
                        2: "MID", 3: "ADC", 4: "SUPPORT"}

        for i, participant in enumerate(participants):
            role = role_indices[i % 5]  # Cycle through roles using modulo
            # Remove "role" and "lane" from participant
            participant.pop("role", None)
            participant.pop("lane", None)
            participants_data.append({
                "gameId": gameId,
                "patch": patch,
                "participantId": participant["participantId"],
                "blueTeam": game_json["blueTeam"],
                "redTeam": game_json["redTeam"],
                # Add the role
                "role": role,
                # Get the data except the data above
                **participant

            })

        return participants_data

    def get_participants_stats_from_game_any_version(self, game_json):
        """
        This method works with any version of the API
        """
        if "gameStartTimestamp" in game_json:
            return self.get_participants_stats_from_game_v5(game_json)
        else:
            return self.get_participants_stats_from_game_v4(game_json)
