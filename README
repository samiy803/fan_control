# Fan Control for IBM x series servers
A simple script to control the fan speed on IBM x series servers. Since these servers run in a datacenter, noise is not a concern. If you are running these servers at home, you may want to reduce the fan speed to make it quieter. This script will allow you to do that. Some notable features of this script are:
- Written in Python for simplicity
- Compiles to a static binary for reliability incase Python broke (common occurance lmao)
- Uses the IPMI interface to control the fan speed
- Can be run as a daemon to automatically adjust the fan speed based on the temperature
- Uses smoothing to prevent the fan speed from changing too rapidly
- Well documented code for easy modification, you will likely need to modify the script to work with your server
- Tested on IBM x3650 M2, should work on other IBM x series servers (no guarantees)

# Installation
You can run the script directly using Python:
```bash
python3 main.py
```
But it's better to compile it to a static binary. This will make it more reliable and easier to run as a daemon. To compile the script,
take a look at the `compile.sh` script. You will need to modify the script to work with your Python installation. It will create a binary called `fan_control` in your /usr/local/bin directory. You can then run the script as a daemon using systemd. 


# Usage
You can run the script directly as shown above, or run the compiled binary.

To run the script as a daemon, you can use systemd. Here is an example systemd service file:
```ini
[Unit]
Description=Fan Control for IBM x series servers
After=network.target # IPMI requires network to be up

[Service]
Type=simple
ExecStart=/usr/local/bin/fan_control
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

# License
Do whatever you want with this code. Don't blame me if it breaks your server.