# WifiLog
WifiLog is a tool that monitors your internet connection and logs any drops in connectivity. It can be helpful for diagnosing and troubleshooting internet connectivity issues *(and complaining to your ISP)*.
### Features
- Run and go. This script requires basically no setup. You can even set it to launch on boot if you want.
- Checks connectivity by pinging 1.1.1.1, which is more reliable than Windows' tray icon
- Logs network connection changes to a .log file called WifiLog.log, stored right alongside the script. This file can contain multiple sessions at the same time. 
- Generates statistics on connection stability.
- Session Management: The log file can contain multiple sessions, decluttering your desktop.
- Licensed under the MIT License, I encourage community contributions and improvements.
### Usage
- Open a terminal on your project's directory
- `python ./WifiLog-v2.py`
- The program will start logging everything to the file (it will be created if it doesn't exist)
### Quirks (READ!!!)
- The script only works on Windows systems **set to English language**. Other languages (like Spanish) are likely to fail. If it succeeds in your non-english system, please open a ticket
- Make sure to stop with Ctrl + C, otherwise session statistics won't be logged to the file.
### Requirements:
- **Python** (I'm using version 3.11.8)
- **Windows** (English language only)
### Extra
#### Broken UI
If the UI breaks:
- Use Windows Terminal, which supports ANSI escape sequences, instead of the regular terminal.
- It's very buggy on small terminal sizes. If the UI breaks, make your terminal bigger. *(I won't work on this issue, but if you fix this issue I will happily accept your PR)*
#### Set script to autostart
- Create a txt file and name it start.bat (the icon should change to a window with cogs)
- Inside it, put the following code: `python ./WifiLog-v2.py`
- Right click your script --> Show more options --> Send to --> Desktop (create shortcut)
- Win + R --> shell:startup --> [Enter] --> Drag shortcut from desktop to folder
