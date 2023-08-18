# Leaguepedia Client and Stats Parser

This is a NON-OFFICIAL client for the Leaguepedia API. It is written in Python 3.11 and is currently in development.
The stats parser class allows you to get stats from a Leaguepedia page and to parse them into a dictionary.
It doesn't care about the version of the API of the game.

## Installation

### From source

To install the client, run the following command:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Then you just have to import the client in your project:

```python
from lib.leaguepedia_client import LeaguepediaClient
from lib.stats_parser import StatsParser
```

## Usage

From now, I created few scripts to allow me to test the client and the parser. You can find them in the root folder.
To use them, you just have to run the following command:

```bash
python3 <script_name>.py
```

# TODO List

With no order of priority:

- [ ] Make a possibility to select directly the attributes you want to save from the stats parser
- [ ] Make an analysis of the stats from the tournaments and make a rating of the players
- [ ] Visualize the stats of the players in a web page
- [ ] Probably store the stats in a database
