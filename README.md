# crassh ![Build Status](https://travis-ci.org/linickx/crassh.svg?branch=tests-beta)

Cisco Remote Automation via SSH (*or C.R.A.SSH for short*) is a python script for automating commands on Cisco devices.

## Installation ##

You'll need both python and [paramiko](https://github.com/linickx/crassh/blob/master/README.md#aob), once you have both of those just [download crassh.py direct from github](https://raw.githubusercontent.com/linickx/crassh/master/crassh.py) and save it somewehere ( *like $HOME/bin* ), e.g.

```
curl -k -o crassh.py https://raw.githubusercontent.com/linickx/crassh/master/crassh.py
chmod +x crassh.py
```

## Usage ##

Usage is quite straight forward, `./crassh.py` and there's a built in help with `-h`, e.g :

```
linickx:crassh nick$ ./crassh.py -h


Nick's Cisco Remote Automation via Secure Shell - Script, or C.R.A.SSH for short!

Usage: ./crassh.py -s switches.txt -c commands.txt -p -w -t 45 -e
   -s supply a text file of switch hostnames or IP addresses [optional]"
   -c supply a text file of commands to run on switches [optional]"
   -w write the output to a file [optional | Default: True]"
   -p print the output to the screen [optional | Default: False]"
   -pw is supported, will print the output to screen and write the output to file! [optional]"
   -t set a command timeout in seconds [optional | Default: 60]"
   -X disable \"do no harm\" [optional]"
   -e set an enable password [optional]"
   -d set a delay between commands [optional]"

Version: 1.11

linickx:crassh nick$
```

### Input files ###

The `-s` option allows you to feed in a *switch* file, i.e. a list of devices to connect to, the format is simple, one device per line, (either IP addresses or resolvable names is fine) eg:

```
192.168.1.72
coreswitch.domain.local
accessswitch1.domain.local
```

The `-c` option allows you to run multiple commands, for example:

```
show ver
show log
```

You can even make config changes:

```
conf t
interface GigabitEthernet1/9
description *** UNUSED ***
```

If you want to mix *config* commands with *show* commands then you need to include _*exits*_, e.g:

```
show run int g1/9
conf t
interface GigabitEthernet1/9
description *** UNUSED ***
exit
exit
show run int g1/9
```

### Do no Harm ###

crassh has a very basic safe mode, i.e. to stop users reloading all their switches on the network at once; if that is something you really _really_ want to do then `-X` is what you need!

### Print Vs Write ###

By default, crassh will write it's output to a file, in the format hostname-YearMonthDate-HourMinuteSecond. If you suppy the `-p` option, crassh will output to screen instead. If you want to Print and Write, use `-pw`

### Execution Timeout ###

Let's say you run a command that take a long time, say a million pings, crassh will wait for 60 seconds for the command to complete and then bail and move on to the next command - this should be fine for most commands. If you do actually want to send a million pings, then use the `-t` option to extend the timeout ( *i.e how long crassh will wait* )

## AoB ##

I've written a [tutorial here](http://www.linickx.com/3980/automating-cisco-commands-with-c-r-a-ssh) on how to use crassh. Future [news about crassh can be found here](http://www.linickx.com/tag/crassh).

### Paramiko on Linux ###

For debian/ubuntu boxes

   `sudo apt-get install python-paramiko`

For redhat/fedora boxes

   `sudo yum install python-paramiko`

### Paramiko on OS X ###

For apples, get homebrew setup and then

   `brew install python`  
   `pip install paramiko`

### Paramiko on Windows ###

For windohz boxes, it's a bit more complicated.

* Download and install [Visual Studio C++ 2008 Express Edition](http://download.microsoft.com/download/A/5/4/A54BADB6-9C3F-478D-8657-93B3FC9FE62D/vcsetup.exe) ( *do not install SQL* )
* Install [Python 2.7.8 – Select the correct MSI](https://www.python.org/download/releases/2.7.8/) for your architecture
* Download [get-pip.py](https://bootstrap.pypa.io/get-pip.py) ( *Don’t use Internet Explorer it will mangle the file; _use Firefox_ to download.* )
* Open an **Administrator** command prompt and run `“c:\Python27\python.exe get-pip.py“`
* From the same admin prompt, run `“C:\Program Files\Microsoft Visual Studio 9.0\Common7\Tools\vsvars32.bat”` ( *that's for 32bit machines… or for 64bit machines, run* `“C:\Program Files (x86)\Microsoft Visual Studio 9.0\Common7\Tools\vsvars64.bat“`)
* From the same admin prompt, run `“c:\Python27\Scripts\pip install paramiko“`


### Disclaimer ###

The word *Cisco* is used as a description because this script should work with any Cisco IOS device. Cisco is a registered trademark of Cisco Systems Inc; this script is not associated, endorsed, supported or affiliated in any way with Cisco and none of these are implied.
