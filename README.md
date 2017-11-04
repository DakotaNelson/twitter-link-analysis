# Twitter Link Analysis

Find out what links are shared most by your twitter followees (the people you follow). First, grabs a list of the people you follow, then uses the Twitter streaming API to return any Tweet from them that has a link in it (in realtime!). These tweets are then stored in a quick-n-dirty SQLite database for analysis.

### Quickstart

Copy `config-template.py` to `config.py` and fill in the required parameters, then `python run.py` and watch the links roll in. They're printed to the screen and also saved in a sqlite database - you'll see the database appear on its own once you get everything running.

### Todo

- [ ] Analysis code you can run to generate reports on what domains are the most shared.
