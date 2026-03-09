# Copilot Quota
A CLI and MenuBar tool to show you how much of your quota should be used by the end of the day. Quota is based on weekday usage and accounts for federal holidays.

To persist the menu bar app, modify the path to the `copilot_quota.py` file in the `copilot.plist` file. Then copy/move the file to `~/Library/LaunchAgents/com.github.randy.copilot-quota.plist`. Finally, run `launchctl load ~/Library/LaunchAgents/com.github.randy.copilot-quota.plist`. 
