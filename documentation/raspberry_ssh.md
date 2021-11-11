# Connecting to Raspberry Pi via SSH

To interface a Raspberry Pi (or other linux computer) through a network, a common protocol is SSH. This guide will show both how to use SSH in a regular shell, and using Visual Studio Code for easier remote code-editing.

The Pi (for this project) will connect to any WiFi access point with the SSID `op7pro` and password `peterkrull`.

## Using SSH via shell

*Note for Windows*
Later versions of Windows have `PowerShell` as an alternative to the `Command Prompt` that supports SSH natively.

First, acquire the the IP-address of the Raspberry Pi. Then open `PowerShell` or the `Linux terminal` and enter the following, where `user` is the user on the machine you wish to access, and `ip` is the IP-address of the machine:

```bash
ssh user@ip
```

For this project, the user is `pi`, and the ip is (usually) `192.168.43.202`, so:

```bash
ssh pi@192.168.43.202
```

Then you will be asked to enter a password for the user. The default password for the `pi` user in Raspberry OS is `raspberry`.

## Using Visual Studio Code

In Visual Studio Code, go to the `Extensions` panel on the left side, and search for `SSH` and download the one called `Remote - SSH` by Microsoft. Press `Shift, Ctrl, P` to bring up the command pallette and search for `Remote-SSH: Connect to Host...`, press enter. In the text field, write the following, where `user` is the user on the machine you wish to access, and `ip` is the IP-address of the machine:

```bash
user@ip
```

For this project, the user is `pi`, and the ip is (usually) `192.168.43.202`, so:

```bash
pi@192.168.43.202
```

In the left panel, select `Explorer` (top button in panel) and select an appropriate folder on the remote machine to work on.