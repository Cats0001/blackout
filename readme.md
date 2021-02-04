__Blackout v0.1.3__
***
Blackout is a tool that can be used to disable certain categories of devices on a local network.
It utilizes similar technologies to parental-control devices (ARP Spoofing/Poisoning) in order to selectively deny 
access to the outside web. Blackout is still in its early stages, please do not expect all features described to be completed. Features requiring 
additional work for basic functionality will be annotated with a triple asterisk (__***__)

Devices are blocked via two methods:
1. Denying all traffic from a certain IP address
2. Denying access to certain URLs from an ip addresses __***__

Option 1 is good for cases where a device can clearly be identified on the network, and is more resistant to software
changes by the OEM. Option 2 works in cases where a device is more difficult to detect, or where it could be a device
you would not wish to disable.

Currently, the list of devices is very minimal, and is really restricted to what I am personally able to test with.
If you wish to add your own device feel free to open a pull request, or open an issue with the following information:
1. Hostname (as shown in nmap)
2. Vendor (as shown in nmap)
3. URLs which this device connects to

***
Installation (Source):
1. Install nmap (https://nmap.org/download.html)
2. Clone / Download this repo
3. Install requirements.txt

***
Usage:

```
cd /blackout/main.py/dir/goes/here
python main.py

...
```


Single Device Modes:
1. NO ICE CREAM FOR U  __***__
   1. Disable smart fridges. 
   2. If there is such a thing as a smart coffee machine, I will * somehow * make
      blackout intercept those requests with 418's.
2. LIGHTS OUT
    1. Disable smart cameras
3. DING DONG  __***__
    1. Disable smart doorbells
4. LOCKED OUT 
    1. Disable smart locks (currently only MyQ garage door, please submit data.)
5. CONTAINMENT BREACH  __***__
    1. Disable smart security systems
6. TIMMY  __***__
    1. Disable parental control systems
7. DIALTONE
   1. Disable phones, currently only works on Apple devices. May also take out some Apple TVs and Macbooks.
    
Multi Device Modes:

1. GHOST  __***__
    1. Disables all monitoring systems (Cameras, Doorbells, Security, Parental Controls)
    
2. EXFIL  __***__
    1. Disables Cameras, Doorbells, Security, and Locks. Perfect for a quick getaway.
    
2. HAIL_MARY
    1. Disables **any** smart device on the network that is covered by the data.py rules.