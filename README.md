# April-Fools-Virus
A small April Fools prank made by yours truly

Uses Tkinter and Python to create popups. Closing a popup will only create more popups, unless the correct password is inputted. Trying to quit using task manager will not work 💀, they will have to either restart their computer or find the password.

Did I mention that the number of popups grows almost exponentially with each close?

# How it works

There are two files, Hydra.py and Watchdog.py. 
- Hyrda.py is where the main magic happens as that is file which creates the popups. It also starts up Watchdog.py
- Watchdog.py is a watchdog, ensures that if the program is quit using task manager that it is reopened. 
- Website folder contains the website which hosts the delivery method. Website downloads the files onto your device. 

# How to create it

You can use the following commands:
- pyinstaller --onefile --windowed --icon=./Images/hydra_logo.icns hydra.py | For Hydra
- pyinstaller --onefile --windowed --icon=./Images/watchdog_logo.icns watchdog.py | For Watchdog  

