# RPi-ifdownCheck
A Python script designed to be run when a network interface (configured in the settings.ini file) changes to 'down' state in order to shutdown the system after a configurable number of seconds as defined in the settings.ini file.

Python script can be enabled by creating a file called '40-RPi-ifdownCheck' (with 644 permissions) in '/lib/dhcpcd/dhcpcd-hooks' folder with the following code:

```
# If Network Interface goes down, run RPi-ifdownCheck Python Script

if $if_down; then
        # Path to Launcher BASH script for Python script
        /root/Git/RPi-ifdownCheck/launcher.sh &
fi
```
