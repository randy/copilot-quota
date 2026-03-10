# Copilot Quota
A CLI and MenuBar tool to show you how much of your quota should be used by the end of the day. Quota is based on weekday usage and accounts for federal holidays.

To run the CLI, do the following:
```
python3 -m venv copilot-env
source copilot-env/bin/activate
pip install workalendar
python3 copilot_quota.py
```

To run the MenuBar app, include `rumps` in the above install like this:
```
pip install workalendar rumps
```

To persist the menu bar app, modify the paths to `python3` and the `copilot_quota.py` file as well as the user info in the `copilot.plist` file. Then copy/move the file to `~/Library/LaunchAgents/com.github.randy.copilot-quota.plist`. Finally, run `launchctl load ~/Library/LaunchAgents/com.github.randy.copilot-quota.plist`. Restart your computer or run `python3 copilot_quota.py &` from the repository's directory.
