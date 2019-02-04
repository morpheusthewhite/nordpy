# NordPy

[![release 1.1](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/morpheusthewhite/NordPy/releases/tag/1.1)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/morpheusthewhite/NordPy/issues)

A python application with gui to connect automatically to the recommended NordVPN server (as of NordVPN site) of a certain type, in a certain country or to the specific chosen server or to choose manually the preferred server (stats for each server are shown in the relative window).

All server types on NordVPN site are available to be selected in the window.

<b> NOTE </b>: ikev2 support is tested on Debian, Arch and derivatives (if something's not right button won't show up)
### Installation and requirements

For <b>Debian/Ubuntu</b>, <b>Fedora/Red Hat</b> and <b>Arch Linux</b> users:

To install all dependencies, download config files and to add a desktop entry in the main menu just run `install.sh`

For <b>other distros</b>:

install the following packages:

```
python3 python3-tk python3-requests openvpn wget unzip
```
and
```
strongswan strongswan-ikev2 libstrongswan-standard-plugins libstrongswan-extra-plugins libcharon-extra-plugins
```
to support ikev2 (facultative)
```
networkmanager-openvpn
```
to support Network Manager (facultative).

Then run `install.sh`

## Usage
Open the application, select your preferred server type (also manually) and protocol and just press connect. Once you are connected you can even close the application and reopen it when you want to disconnect the VPN.
If the size of the window does not fit entirely the gui components change the scale factor in the advanced settings.

#### Additional info
<li> The button "Reset settings" resets only the settings of the connection (each time a VPN connection is established the used options are saved and restored at the next start). </li>
<li> The percent associated to each server in the window for manual choice is the <b>load</b> (a big load implies a slower connection)</li>

#### Advanced Settings

![Alt text](media/screenshots/screen05.png?raw=true "Preview")

<li> Scale Factor: this parameter affects the size of a window (will be restored at each start)</li>
<li> Network Manager: if checked NordPy will try to connect through networkmanager-openvpn plugin (checked by default). Works only if network manager is enabled</li>

#### Previews
![Alt text](media/screenshots/screen01.png?raw=true "Preview")  

When pressed "Select":

![Alt text](media/screenshots/screen03.png?raw=true "Preview")

After connection has been established:

![Alt text](media/screenshots/screen02.png?raw=true "Preview")

Once closed and restarted:  
![Alt text](media/screenshots/screen04.png?raw=true "Preview")
