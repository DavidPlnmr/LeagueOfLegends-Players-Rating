# Leaguepedia Stats Rating

This is a project to rate the players of League of Legends from the stats of the tournaments.
It is mainly inspired by the work of [Xenesis](https://twitter.com/lol_Xenesis).

## Data

The data is taken from the [Leaguepedia](https://lol.gamepedia.com/League_of_Legends_Esports_Wiki) website, more specifically from this [link](https://lol.fandom.com/wiki/Help:ACS_archive_%26_post-game_JSONs#Json_locations)

### Leaguepedia Client

The leaguepedia client is my own client that I used to simplify the requests to the Leaguepedia API.
It is not a complete client, it only has the requests that I needed for this project.
But you can easily make the more common requests using it. Feel free to add more requests to it.

### Stats Parser

The stats parser is a parser that I made to parse the stats from the tournaments. It will take care of the version of the stats. Also it adds few stats like the roles of the players and the champions.

### Stats Rating

The stats rating are made in the notebook `stats_rating.ipynb`. It is a notebook that I used to make the rating of the players. My goal is to document it and make it more readable.

## Installation

Firstly, make a virtual environment and activate it.

```bash
python3 -m venv venv
source venv/bin/activate
```

Then install the requirements.

```bash
pip install -r requirements.txt
```

## Usage

You can use the 'fetching_multiple_tournaments.py' script to fetch the stats of multiple tournaments.

```bash
python fetching_multiple_tournaments.py
```

Otherwise, you can use the 'fetching_tournament.py' script to fetch the stats of a single tournament.
Don't forget to follow the instructions in the script.

```bash
python fetching_tournament.py
```

Note : LPL and LJL games stats can't be fetched because they are played in a special server.

# TODO List

With no order of priority:

- [x] Make an analysis of the stats from the tournaments and make a rating of the players
- [ ] Visualize the stats of the players in a web page
- [ ] Probably store the stats in a database
