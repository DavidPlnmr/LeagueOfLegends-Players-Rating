from leaguepedia_client import LeaguepediaClient

client = LeaguepediaClient()
# print(client.get_current_regions())

print(client.get_tournaments(name__contains="Worlds",
      date__gt="2019-01-01", date__lt="2020-01-01"))
