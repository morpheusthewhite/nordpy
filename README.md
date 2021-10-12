# NordPy

[![release 1.3.4](https://img.shields.io/github/tag/morpheusthewhite/nordpy.svg?style=flat)](https://github.com/morpheusthewhite/NordPy/releases/tag/1.3.4)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/morpheusthewhite/NordPy/issues)
[![contributions welcome](https://img.shields.io/github/license/morpheusthewhite/nordpy.svg?style=flat)](https://github.com/morpheusthewhite/NordPy/blob/master/LICENSE)

A python application with gui to connect automatically to the recommended NordVPN server (as of NordVPN site) of a certain type, in a certain country or to the specific chosen server (stats for each server are shown in the relative window).

All server types on NordVPN site are available to be selected in the window.

KDE Plasma users can also find [the relative plasmoid](https://github.com/morpheusthewhite/nordpy-plasmoid).

<b>Tested against DNS leaks (NetworkManager use is discouraged (and disabled by default) as it may leak DNS)</b>

<b> NOTE </b>: ikev2 support is tested on Debian, Arch and derivatives (if something's not right button won't show up)

## Features

- Automatic connection to recommended server (according to nordvpn.com)
- TCP, UDP and IKEv2/IPsec protocols are available
- Connection (TCP and UDP) can be established with either `openvpn` or `NetworkManager-openvpn` (will show connection in the system interface)
- No DNS leak (when using `openvpn`)
- Killswitch (when using `openvpn`)
- Quick connection/disconnection from command line (according to last chosen server type)
- Easy to setup for [autoconnection](#autostart) at startup
- Integrated with its own [plasmoid](https://github.com/morpheusthewhite/nordpy-plasmoid)

## Installation and requirements

<b>Arch Linux</b> users can find this project on the [AUR](https://aur.archlinux.org/packages/nordpy/).

For <b>Debian/Ubuntu</b>, <b>Fedora/Red Hat</b> users:

To install all dependencies, download config files and to add a desktop entry in the main menu just run `install.sh`

For <b>other distros</b>:

install the following packages:

```
python3 python3-tk python3-requests openvpn wget unzip net-tools iproute2
```
and
```
strongswan libstrongswan-standard-plugins libstrongswan-extra-plugins libcharon-extra-plugins
```
to support ikev2 (facultative)
```
networkmanager-openvpn
```
to support Network Manager (facultative).

Then run `install.sh`

If you have a dual monitor setup you may also want to install `screeninfo` (`pip3
install --user screeninfo`) to correct window centering.

### Installing with support for obfuscated servers

At the launch of the installation script you will be asked

```
Do you want to install support for obfuscated servers (it will reinstall openvpn)?[y/n] (Recommended: n)
```

if you answer is `y` then openvpn will be built from source (version 2.4.4) applying patch for obfuscation. If you do not run Debian/Ubuntu, Fedora or Arch, you should provide the following packages and then run `install.sh`

```
automake autoconf perl gnupg quilt libtool openssl-devel lzo-devel pam-devel net-tools
```

<b>Note</b>: Installing support for obfuscated servers breaks Network Manager openvpn support in some distros (in that case you should disable it in the advanced options)

## Usage
Open the application, select your preferred server type (also manually) and protocol and just press connect. Once you are connected you can even close the application and reopen it when you want to disconnect the VPN.
If the size of the window does not fit entirely the gui components change the scale factor in the advanced settings.

#### Additional info
<li> The button "Reset settings" resets only the settings of the connection (each time a VPN connection is established the used options are saved and restored at the next start). </li>
<li> The percent associated to each server in the window for manual choice is the <b>load</b> (a big load implies a slower connection)</li>

#### Advanced Settings

![Alt text](media/screenshots/screen05.png?raw=true "Preview")

<li> Scale Factor: this parameter affects the size of a window (will be restored at each start)</li>
<li> Network Manager: if checked NordPy will try to connect through networkmanager-openvpn plugin (disabled by default). Works only if network manager is enabled. It is discouraged the use, as it leaks DNS.</li>


#### Command line interface
`nordpy` can be called with 3 different commands (in this case the gui isn't opened):
- `--quick-connect` starts a connection according to the last chosen preferences (you must first start a connection using the gui)
- `--quick-disconnect` shuts down any connection that `nordpy` previously started 
- `--status` checks if any VPN is already running 

All options can be listed with `nordpy --help`

#### Autostart
You can easily configure `nordpy` to establish VPN connection at the start of your system. You just need to 
1. Install a cron implementation (I usually use `cronie`)
2. Edit the root crontab (`sudo crontab -e`) and add the following line to it

```
@reboot PATH/TO/nordpy.py --quick-connect --wait-connection
```

(you can easily obtain your path to `nordpy` with `which nordpy`).

You can disable it just by deleting the line you added to the crontab.

### Previews
![Alt text](media/screenshots/screen01.png?raw=true "Preview")  

When pressed "Select":

![Alt text](media/screenshots/screen03.png?raw=true "Preview")

After connection has been established:

![Alt text](media/screenshots/screen02.png?raw=true "Preview")

Once closed and restarted:  
![Alt text](media/screenshots/screen04.png?raw=true "Preview")

## Development 

### Tests

Before running the tests you need to install needed dependencies with 

```
# pip install -r tests/requirements.txt
```

Make sure you also connected at least once with the gui (in order to store the credentials). Then tests can be started with 

```
$ python -m pytest tests
```

#### Environment

You can also easily setup a test environment with `vagrant` (so you will need to install before proceeding with the following steps): the project contains a minimalistic `Vagrantfile` to initialize it.

1. Start the `nordpy` gui and connect to any server in order to store the password

2. Change the permissions of the `credentials` file. **WARNING**: this will the expose the password of your NordVPN account to anyone which has access to your machine.
```
# chmod +r credentials
```

3. Create the environment

```
$ vagrant up
```

4. Open a shell into the vm

```
$ vagrant ssh
```

5. Move to the shared folder and install nordpy

```
$ cd /Vagrant && ./install.sh
```

6. Start testing as said above!
