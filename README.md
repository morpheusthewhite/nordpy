# NordPy
A python application with gui to connect automatically to the recommended NordVPN server (as of NordVPN site) of a certain type or to the specific chosen server.

All server types on NordVPN site are available to be selected in the window.

**Installation**

For Debian/Ubuntu and Fedora users:

To install all dependencies, download config files and to add a desktop entry in the main menu just run install.sh

For other distro:

install the following packages
```
python3 python3-tkinter python3-requests openvpn wget unzip
```
then run install.sh

**Usage**  
Open the application, select your preferred server type (also manually) and protocol and just press connect. Once you are connected you can even close the application and reopen it when you want to disconnect the VPN.

**Previews**:  
![Alt text](media/screenshots/screen01.png?raw=true "Preview")  
![Alt text](media/screenshots/screen03.png?raw=true "Preview")

When pressed "Select":


![Alt text](media/screenshots/screen02.png?raw=true "Preview")

Once closed and restarted:  
![Alt text](media/screenshots/screen04.png?raw=true "Preview")
