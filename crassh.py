#!/usr/bin/env python
# coding=utf-8

"""Python script to automate running commands on switches.
    Cisco Remote Automation via Secure Shell... or C.R.A.SSH for short!
    
.. currentmodule:: crassh
.. moduleauthor:: Nick Bettison - www.linickx.com
"""

# Import libs
import getpass              # Hide Password Entry
import paramiko             # SSH 
import socket               # TCP/Network/Socket 
import time, datetime       # Date & Times
from io import StringIO     # 
import sys, getopt          # Command line options
import os, stat             # File system
import re                   # Regex

# Version Control in a Variable
crassh_version = "2.5"

# Python 2 & 3 input compatibility
try:
    input = raw_input
except NameError:
    pass

"""
    Functions
"""

def send_command(command = "show ver", hostname = "Switch", bail_timeout = 60):
    """Sending commands to a switch, router, device, whatever!

        Args:
           command (str):  The Command you wish to run on the device.
           
           hostname (str): The hostname of the device (*expected in the* ``prompt``).
           
           bail_timeout (int): How long to wait for ``command`` to finish before giving up.

        Returns:
           str.  A text blob from the device, including line breaks.


        REF: http://blog.timmattison.com/archives/2014/06/25/automating-cisco-switch-interactions/
    """
    global remote_conn, remote_conn_pre
    
    # Start with empty var & loop
    output = ""
    keeplooping = True

    # Regex for either config or enable
    regex = '^' + hostname + '(.*)(\ )?#'
    theprompt = re.compile(regex)

    # Time when the command started, prepare for timeout.
    now = int(time.time())
    timeout = now + bail_timeout

    # Send the command
    remote_conn.send(command + "\n")

    # loop the output
    while keeplooping:

        # Setup bail timer
        now = int(time.time())
        if now == timeout:
            print("\n Command %s took %s secs to run, bailing!" % (cmd, str(bail_timeout)))
            output += "crassh bailed on command: " + cmd
            keeplooping = False
            break

        # update receive buffer whilst waiting for the prompt to come back
        if remote_conn.recv_ready():
            output += remote_conn.recv(2048).decode('utf-8')

            # Search the output for our prompt
            theoutput = output.splitlines()
            for lines in theoutput:
                myregmatch = theprompt.search(lines)

            if myregmatch:
                keeplooping = False

    return output

def do_no_harm(command):
    """Check Commands for dangerous things

    Args:
       command (str):  The Command you wish to run on the device.

    Returns:
       Nothing

    This function will ``sys.exit()`` if an *evil* command is found

    >>> crassh.do_no_harm("show ver")
    >>>

    So, good commands just pass through with no response... maybe I should oneday make it a True/False kind of thing.

    """

    # Innocent until proven guilty
    harmful = False

    # Regex match each "command"
    if re.match("rel", command):
        harmful = True
        error = "reload"

    if re.match("wr(.*)\ e", command):
        harmful = True
        error = "write erase"

    if re.match("del", command):
        harmful = True
        error = "delete"

    if harmful:
        print("")
        print("Harmful Command found - Aborting!")
        print("  \"%s\" tripped the do no harm sensor => %s" % (command, error))
        print("\n To force the use of dangerous things, use -X")
        print_help()

# Simple help print and exit
def print_help(exit = 0):
    """Prints the Help for the CLI tool

    Args:
       exit (int):  Exit Code

    Returns:
       None

    When called this function will ``sys.exit()``

    """

    global crassh_version
    
    print("\n Usage: %s -s switches.txt -c commands.txt -p -w -t 45 -e" % sys.argv[0])
    print("   -s supply a text file of switch hostnames or IP addresses [optional]")
    print("   -c supply a text file of commands to run on switches [optional]")
    print("   -w write the output to a file [optional | Default: True]")
    print("   -p print the output to the screen [optional | Default: False]")
    print("   -pw is supported, will print the output to screen and write the output to file! [optional]")
    print("   -t set a command timeout in seconds [optional | Default: 60]")
    print("   -X disable \"do no harm\" [optional]")
    print("   -Q disable \"quit on failure\" [optional]")
    print("   -e set an enable password [optional]")
    print("   -d set a delay (in seconds) between commands [optional]")
    print("   -A set an Authentication file for SSH credentials [optional]")
    print("   -U set a Username for SSH Authentication [optional]")
    print("   -P set a Password for SSH Authentication [optional]")
    print(" ")
    print("Version: %s" % crassh_version)
    print(" ")
    sys.exit(exit)

def isgroupreadable(filepath):
    """Checks if a file is *Group* readable

    Args:
       filepath (str):  Full path to file

    Returns:
       bool.  True/False

    Example:

    >>> print(str(isgroupreadable("file.txt")))
    True

    REF: http://stackoverflow.com/questions/1861836/checking-file-permissions-in-linux-with-python

    """

    st = os.stat(filepath)
    return bool(st.st_mode & stat.S_IRGRP)

def isotherreadable(filepath):
    """Checks if a file is *Other* readable

    Args:
       filepath (str):  Full path to file

    Returns:
       bool.  True/False

    Example:

    >>> print(str(isotherreadable("file.txt")))
    True

    """

    st = os.stat(filepath)
    return bool(st.st_mode & stat.S_IROTH)

def readtxtfile(filepath):
    """Read lines of a text file into an array
    Each line is stripped of whitepace.
    

    Args:
       filepath (str):  Full path to file

    Returns:
       array.  Contents of file

    Example:

    >>> print(readtxtfile("./routers.txt"))
    1.1.1.1
    1.1.1.2
    1.1.1.3

    
    """
    # Check if file exists
    if os.path.isfile(filepath) == False:
        print("Cannot find %s" % filepath)
        sys.exit()
    # setup return array
    txtarray = []
    # open our file
    f=open(filepath,'r')
    # Loop thru the array
    for line in f:
        # Append each line to array
        txtarray.append(line.strip())
    # Return results
    return txtarray

# Read a Crassh Authentication File
def readauthfile(filepath):
    """Read C.R.A.SSH Authentication File
    
    The file format is a simple, one entry per line, colon separated affair::
    
        username: nick
        password: cisco

    Args:
       filepath (str):  Full path to file

    Returns:
       tuple.  ``username`` and ``password``

    Example:

    >>> username, password = readauthfile("~/.crasshrc")
    >>> print(username)
    nick
    >>> print(password)
    cisco

    """

    # Check if file exists
    if os.path.isfile(filepath) == False:
        print("Cannot find %s" % filepath)
        sys.exit()
    # Open file
    f=open(filepath,'r')
    # Loop thru the array
    for fline in f:
        thisline = fline.strip().split(":")
        if thisline[0].strip() == "username":
            username = thisline[1].strip()
        if thisline[0].strip() == "password":
            if isgroupreadable(filepath):
                print("** Password not read from %s - file is GROUP readable ** " % filepath)
            else:
                if isotherreadable(filepath):
                    print("** Password not read from %s - file is WORLD readable **"% filepath)
                else:
                    password = thisline[1].strip()
                    return username, password

def connect(device = "127.0.0.1", username = "cisco", password = "cisco", enable = False, enable_password = "cisco", sysexit = False):
    """Connect and get Hostname of Cisco Device
    
    This function wraps up ``paramiko`` and returns the hostname of the **Cisco** device. The function creates two global variables ``remote_conn_pre`` and ``remote_conn`` which are the paramiko objects for direct manipulation if necessary.
    
    Args:
       device (str):  IP Address or Fully Qualifed Domain Name of Device
       
       username (str): Username for SSH Authentication
       
       password (str): Password for SSH Authentication
       
       enable (bool): Is enable going to be needed? 
       
       enable_password (str): The enable password
       
       sysexit (bool): Should the connecton exit the script on failure? 

    Returns:
       str.  The hostname of the device

    Example:

    >>> hostname = connect("10.10.10.10", "nick", "cisco")
    >>> print(hostname)
    r1
    
    REF: 
        * https://pynet.twb-tech.com/blog/python/paramiko-ssh-part1.html
        * http://yenonn.blogspot.co.uk/2013/10/python-in-action-paramiko-handling-ssh.html

    """
    
    # Global variables - Paramiko Stuff.
    global remote_conn_pre, remote_conn
    
    """
        

    """

    # Create paramiko object
    remote_conn_pre = paramiko.SSHClient()
    # Change default paramiko object settings
    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print("Connecting to %s ... " % device)

    try: 
        remote_conn_pre.connect(device, username=username, password=password, allow_agent=False, look_for_keys=False)
    except paramiko.AuthenticationException as e:
        print("Authentication Error: %s" % e)
        if sysexit:
            sys.exit()
        return False
    except paramiko.SSHException as e:
        print("SSH Error: %s" % e)
        if sysexit:
            sys.exit()
        return False
    except socket.error as e:
        print("Connection Failed: %s" % e)
        if sysexit:
            sys.exit()
        return False
    except:
        print("Unexpected error:", sys.exc_info()[0])
        if sysexit:
            sys.exit()
        return False

    # Connected! (invoke_shell)
    remote_conn = remote_conn_pre.invoke_shell()

    # Flush buffer.
    output = remote_conn.recv(1000)

    # If we have enable password, send it.
    if enable:
        remote_conn.send("enable\n")
        time.sleep(0.5)
        remote_conn.send(enable_password + "\n")

    # Disable <-- More --> on Output
    remote_conn.send("terminal length 0\n")
    time.sleep(0.5)
    # Flush buffer.
    output = remote_conn.recv(1000)

    # Clear the Var.
    output = ""

    # Ok, let's find the device hostname
    remote_conn.send("show run | inc hostname \n")
    while not "#" in output:
        # update receive buffer
            output += remote_conn.recv(1024).decode('utf-8')

    for subline in output.splitlines():
        thisrow = subline.split()
        try:
            gotdata = thisrow[1]
            if thisrow[0] == "hostname":
                hostname = thisrow[1]
                prompt = hostname + "#"
        except IndexError:
            gotdata = 'null'
    
    # Found it! Return it!
    return hostname

def disconnect():
    """Disconnect an SSH Session
    
    Crassh wrapper for paramiko disconnect
    
    No Argumanets, disconnects the current global variable ``remote_conn_pre``
    """
    
    global remote_conn_pre
    remote_conn_pre.close()

def main():
    """Main Code Block
    
    This is the main script that Network Administrators will run.
    
    No Argumanets. Input is used for missing CLI Switches.
    """
    
    # import Global Vars
    global input
    
    # Main Vars (local scope)
    switches = [] # Switches, devices, routers, whatever!
    commands = [] 
    filenames = []
    sfile='' # Switch File
    cfile='' # Command File
    
    # Default variables (values)
    play_safe = True
    enable = False
    delay_command = False
    writeo = True
    printo = False
    bail_timeout = 60
    sysexit = True

    # Default Authentication File Path
    crasshrc = os.path.expanduser("~") + "/.crasshrc"

    # Get script options - http://www.cyberciti.biz/faq/python-command-line-arguments-argv-example/
    try:
        myopts, args = getopt.getopt(sys.argv[1:],"c:s:t:d:A:U:P:hpwXeQ")
    except getopt.GetoptError as e:
        print ("\n ERROR: %s" % str(e))
        print_help(2)

    for o, a in myopts:
        if o == '-s':
            sfile=a
            switches = readtxtfile(sfile)

        if o == '-c':
            cfile=a
            commands = readtxtfile(cfile)

        if o == '-t':
            bail_timeout=int(a)

        if o == '-h':
            print("\n Nick\'s Cisco Remote Automation via Secure Shell - Script, or C.R.A.SSH for short! ")
            print_help()

        if o == '-p':
            writeo = False
            printo = True

        if o == '-w':
            writeo = True

        if o == '-X':
          play_safe = False
        
        if o == '-Q':
          sysexit = False

        if o == '-e':
          enable = True

        if o == '-d':
            delay_command = True
            delay_command_time=int(a)
        
        if o == '-A':
            crasshrc=str(a)

        if o == '-U':
            username=str(a)

        if o == '-P':
            password=str(a)

    # See if we have an Authentication File
    if os.path.isfile(crasshrc) == True:
        try:
            username, password = readauthfile(crasshrc)
        except:
            pass
    
    # Do we have any switches?
    if sfile == "":
        try:
            iswitch = input("Enter the switch to connect to: ")
            switches.append(iswitch)
        except:
            sys.exit()

    # Do we have any commands?
    if cfile == "":
        try:
            icommand = input("The switch command you want to run: ")
            commands.append(icommand)
        except:
            sys.exit()

    """
        Check the commands are safe
    """
    if play_safe:
        for command in commands:
            do_no_harm(command)
    else:
        print("\n--\n Do no Harm checking DISABLED! \n--\n")

    """
        Capture Switch log in credentials...
    """

    try: 
        username
    except:
        try:
            username = input("Enter your username: ")
        except:
            sys.exit()

    try:
        password
    except:
        try:
            password = getpass.getpass("Enter your password:")
        except:
            sys.exit()

    if enable:
        try:
            enable_password = getpass.getpass("Enable password:")
        except:
            sys.exit()


    """
        Time estimations for those delaying commands
    """
    if delay_command:
        time_estimate = datetime.timedelta(0,(len(commands) * (len(switches) * 2) * delay_command_time)) + datetime.datetime.now()
        print(" Start Time: %s" % datetime.datetime.now().strftime("%H:%M:%S (%y-%m-%d)"))
        print(" Estimatated Completion Time: %s" % time_estimate.strftime("%H:%M:%S (%y-%m-%d)"))

    """
        Progress calculations - for big jobs only
    """
    if (len(commands) * len(switches)) > 100:
        counter = 0

    """
        Ready to loop thru switches
    """

    for switch in switches:
        
        if enable:
            hostname = connect(switch, username, password, enable, enable_password, sysexit)
        else:
            hostname = connect(switch, username, password, False, "", sysexit)
                
        if str(hostname) != str("False"):

            # Write the output to a file (optional) - prepare file + filename before CMD loop
            if writeo:
                filetime = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
                filename = hostname + "-" + filetime + ".txt"
                filenames.append(filename)
                f = open(filename,'a')

            # Command Loop
            for cmd in commands:

                # Send the Command
                print("%s: Running: %s" % (hostname, cmd))
                output = send_command(cmd, hostname, bail_timeout)

                # Print the output (optional)
                if printo:
                    print(output)
                if writeo:
                    f.write(output)

                # delay next command (optional)
                if delay_command:
                    time.sleep(delay_command_time)

                # Print progress
                try:
                    counter
                    # Random calculation to find 10 percent
                    if (counter % 10) == 0:
                        completion = ( (float(counter) / ( float(len(commands)) * float(len(switches)))) * 100 )
                        if int(completion) > 9:
                            print("\n  %s%% Complete" % int(completion))
                            if delay_command:
                                time_left = datetime.timedelta(0, (((int(len(commands)) * int(len(switches))) + (len(switches) * 0.5)) - counter)) + datetime.datetime.now()
                                print("  Estimatated Completion Time: %s" % time_left.strftime("%H:%M:%S (%y-%m-%d)"))
                            print(" ")
                    counter += 1
                except:
                    pass


            # /end Command Loop

            if writeo:
                # Close the File
                f.close()


            # Disconnect from SSH
            disconnect()

            if writeo:
                print("Switch %s done, output: %s" % (switch, filename))
            else:
                print("Switch %s done" % switch)

            # Sleep between SSH connections
            time.sleep(1)

    print("\n") # Random line break

    print(" ********************************** ")
    if writeo:
        print("  Output files: ")

        for ofile in filenames:
            print("   - %s" % ofile)

        print(" ---------------------------------- ")
    print(" Script FINISHED ! ")
    if delay_command:
        print(" Finish Time: %s" % datetime.datetime.now().strftime("%H:%M:%S (%y-%m-%d)"))
    print(" ********************************** ")

# If run from interpreter, run main code function.
if __name__ == "__main__":
    main()