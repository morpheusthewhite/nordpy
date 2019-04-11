# NordPy

[![release 1.1](https://img.shields.io/github/tag/morpheusthewhite/nordpy.svg?style=flat)](https://github.com/morpheusthewhite/NordPy/releases/tag/1.1)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/morpheusthewhite/NordPy/issues)
[![contributions welcome](https://img.shields.io/github/license/morpheusthewhite/nordpy.svg?style=flat)](https://github.com/morpheusthewhite/NordPy/blob/master/LICENSE)

A python application with gui to connect automatically to the recommended NordVPN server (as of NordVPN site) of a certain type, in a certain country or to the specific chosen server or to choose manually the preferred server (stats for each server are shown in the relative window).

All server types on NordVPN site are available to be selected in the window.

<b>Tested against DNS leaks (NetworkManager use is discouraged (and disabled by default) as it leaks DNS)</b>

<b> NOTE </b>: ikev2 support is tested on Debian, Arch and derivatives (if something's not right button won't show up)

## Installation and requirements

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

#### Previews
![Alt text](media/screenshots/screen01.png?raw=true "Preview")  

When pressed "Select":

![Alt text](media/screenshots/screen03.png?raw=true "Preview")

After connection has been established:

![Alt text](media/screenshots/screen02.png?raw=true "Preview")

Once closed and restarted:  
![Alt text](media/screenshots/screen04.png?raw=true "Preview")

## Caveat

NordPy will not work on Fedora 29 since launching a `tkinter.OptionMenu`
will cause the application to crash with `Floating point exception (core dumped)`.

For more info and bug progress see [the bug I reported](https://bugzilla.redhat.com/show_bug.cgi?id=1699049)
and [the entire discussion](https://github.com/morpheusthewhite/NordPy/issues/17) on the issues page.


