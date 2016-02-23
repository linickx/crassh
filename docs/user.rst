User Guide
##########

The following documentation is intended for Network Administrators. Crassh provides a way of automating commands on Cisco IOS devcies, that being either lots of commands on one device, one command on lots or devices, or a combination of both.

No Python, programming or scripting knowledge is required to run crassh, it is simply a command line tool that you run on your local PC/Laptop

My `personal blog`_ contains a `tutorial here`_ on how to use crassh in standalone mode which is a subset of the documentation found here.

Assuming that you have performed a standalone installation, the script would be run from the current directory and is quite straight forward, ``./crassh``.

If you have installed crassh via pip, the crassh command should be available without the ``./``

Crassh has a version specific built in help with ``-h``, e.g ::

    linickx:crassh nick$ ./crassh -h


    Nick's Cisco Remote Automation via Secure Shell - Script, or C.R.A.SSH for short!

    Usage: ./crassh -s switches.txt -c commands.txt -p -w -t 45 -e
       -s supply a text file of switch hostnames or IP addresses [optional]"
       -c supply a text file of commands to run on switches [optional]"
       -w write the output to a file [optional | Default: True]"
       -p print the output to the screen [optional | Default: False]"
       -pw is supported, will print the output to screen and write the output to file! [optional]"
       -t set a command timeout in seconds [optional | Default: 60]"
       -X disable \"do no harm\" [optional]"
       -Q disable \"quit on failure\" [optional]"
       -e set an enable password [optional]"
       -d set a delay between commands [optional]"
       -A set an Authentication file for SSH credentials [optional]
       -U set a Username for SSH Authentication [optional]
       -P set a Password for SSH Authentication [optional]

    Version: 2.04

    linickx:crassh nick$

Input files
-----------

The ``-s`` option allows you to feed in a *switch* file, i.e. a list of devices to connect to, the format is a simple plain text file (``*.txt``), one device per line, (*either IP addresses or resolvable names is fine*) eg::

    192.168.1.72
    coreswitch.domain.local
    accessswitch1.domain.local

The ``-c`` option allows you to run multiple commands; same format as before, a simple plain text file (``*.txt``), one command per line. For example::

    show ver
    show log

You can even make config changes::

    conf t
    interface GigabitEthernet1/9
    description *** UNUSED ***

If you want to mix *config* commands with *show* commands then you need to include **exits** , e.g::

    show run int g1/9
    conf t
    interface GigabitEthernet1/9
    description *** UNUSED ***
    exit
    exit
    show run int g1/9

Authentication
--------------

By default crassh will prompt for username and password credentials; ``-U`` can be used to supply a username as a CLI option, ``-P`` can be used to supply a password.   
**Please take note that ``-P`` may expose your password in the command line history**

 
crassh will look for and read a ``~/.crasshrc`` file; currently the file supports two colon separated variables ``username`` and ``password``::

    username: nick
    password: mysecretpass

**STORING YOUR PASSWORD IN PLAIN TEXT IN ``~/.crasshrc`` IS A SECURITY RISK** Please appropriately secure your system; crassh will perform a basic file permission check.

The ``-A`` option can be used to specify different authentication files, for example ``-A /var/secrets/router_credentials.txt``
 

Do no Harm
----------

crassh has a very basic safe mode, i.e. to stop users reloading all their switches on the network at once; if that is something you really *really* want to do then ``-X`` is what you need!

Print Vs Write
--------------

By default, crassh will write it's output to a file, in the format hostname-YearMonthDate-HourMinuteSecond. If you suppy the ``-p`` option, crassh will output to screen instead. If you want to Print and Write, use ``-pw``

Quit on Failure
---------------

crassh by default will stop in it's tracks (quit/exit) if there is a connectivity failure to a device, this is to stop invalid credentials hammering a list of devices and potentially locking out TACACS accounts. **BUT** this also means that if there is network error (*i.e. TCP/IP connectivity issue*) then crassh will also stop, the ``-Q`` option can be used to disable `Quit on Failure`

Execution Timeout
-----------------

Let's say you run a command that take a long time, say a million pings, crassh will wait for 60 seconds for the command to complete and then bail and move on to the next command - this should be fine for most commands. If you do actually want to send a million pings, then use the ``-t`` option to extend the timeout ( *i.e how long crassh will wait* )


.. Links
.. _`personal blog`: http://www.linickx.com
.. _`tutorial here`: http://www.linickx.com/3980/automating-cisco-commands-with-c-r-a-ssh