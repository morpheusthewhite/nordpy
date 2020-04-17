---
name: Bug report
about: Create a report to help us improve
title: ''
labels: ''
assignees: ''

---

**Before Posting an issue**
Make sure you have the last version of NordPy installed, that you installed all needed dependencies and that you run `install.py` with no error and no one posted the same question [here](https://github.com/morpheusthewhite/NordPy/issues) 

**Describe the bug**
A clear and concise description of what the bug is.

If you encountered a connectivity problem, provide the following informations (otherwise just skip them):
1. `ping 8.8.8.8` to verify connection, `ping www.github.com` to verify also DNS
2. Paste here the content of `/etc/resolv.conf`, the output of `ip r` and the output of `iptables --list` (may need root privileges)
3. Connect to VPN and do the same step again, as above
4. Disconnect and again do as above

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Desktop (please complete the following information):**
 - Linux Distribution
 - NordPy version (`git log --pretty=format:'%H' -n 1`)

**Additional context**
Add any other context about the problem here.
