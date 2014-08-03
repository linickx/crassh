#!/usr/bin/python

"""
    Nick Bettison

    Python script to automate running commands on switches.

    Cisco Remote Automation via Secure Shell... or C.R.A.SSH for short!

    Use the -h for help

    - www.linickx.com

"""

# Import libs
import getpass
import paramiko
import time
import datetime
import cStringIO
import sys, getopt
import os.path

# Version Control in a Variable
crassh_version = "1.02"

# Default Vars
sfile=''
cfile=''
switches = []
commands = []
filenames = []
writeo = True
printo = False
bail_timeout = 60

# Functions

# # http://blog.timmattison.com/archives/2014/06/25/automating-cisco-switch-interactions/
def send_command(command, prompt = "#", bail_timeout = 60):
    # Start with empty var
    output = ""
    # Time when the command started, prepare for timeout.
    now = int(time.time())
    timeout = now + bail_timeout

    # Send the command
    remote_conn.send(command + "\n")

    while not prompt in output:
        # update receive buffer whilst waiting for the prompt to come back
        output += remote_conn.recv(1024)
        now = int(time.time())
        if now == timeout:
           print "\n Command \"" + cmd + "\" took " + str(bail_timeout) + "secs to run, bailing!"
           output += "crassh bail: " + prompt

    return output

# Get script options - http://www.cyberciti.biz/faq/python-command-line-arguments-argv-example/

try:
    myopts, args = getopt.getopt(sys.argv[1:],"c:s:t:hpw")
except getopt.GetoptError as e:
    print (str(e))
    print("Usage: %s -s switches.txt -c commands.txt -t timeout" % sys.argv[0])
    sys.exit(2)

for o, a in myopts:
    if o == '-s':
        sfile=a
        if os.path.isfile(sfile) == False:
            print("Cannot find %s" % sfile)
            sys.exit()
        # open our file
        f=open(sfile,'r')
        # Loop thru the array
        for fline in f:
            # Assume one switch per line
            thisswitch = fline.strip()
            switches.append(thisswitch)

    if o == '-c':
        cfile=a
        if os.path.isfile(cfile) == False:
            print("Cannot find %s" % cfile)
            sys.exit()
        # open our file
        f=open(cfile,'r')
        # Loop thru the array
        for fline in f:
            # Assume one switch per line
            thiscmd = fline.strip()
            commands.append(thiscmd)

    if o == '-t':
        bail_timeout=int(a)

    if o == '-h':
        print("\n")
        print("Nick\'s Cisco Remote Automation via Secure Shell - Script, or C.R.A.SSH for short! ")
        print(" ")
        print("Usage: %s -s switches.txt -c commands.txt -p -w -t 45" % sys.argv[0])
        print("   -s is optional, run without -s for a single switch")
        print("   -c is optional, run without -c for a single command")
        print("   -w is optional, use to write the output to a file [Default: True]")
        print("   -p is optional, use to print the output to a file [Default: False]")
        print("   -pw is supported, optional and will print the output to screen and write the output to file!")
        print("   -t is optional, use to set a command timeout in seconds [Default: 60]")
        print(" ")
        print("Version: %s" % crassh_version)
        print(" ")
        sys.exit()

    if o == '-p':
        writeo = False
        printo = True

    if o == '-w':
        writeo = True


if sfile == "":
    iswitch = raw_input("Enter the switch to connect to: ")
    switches.append(iswitch)

if cfile == "":
    icommand = raw_input("The switch command you want to run: ")
    commands.append(icommand)

"""
    Capture Switch log in credentials...
"""

username = raw_input("Enter your username: ")
password = getpass.getpass("Enter your password:")

"""
    Ready to loop thru switches
"""

for switch in switches:
    """
        https://pynet.twb-tech.com/blog/python/paramiko-ssh-part1.html

    """

    remote_conn_pre = paramiko.SSHClient()

    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    remote_conn_pre.connect(switch, username=username, password=password)

    remote_conn = remote_conn_pre.invoke_shell()

    output = remote_conn.recv(1000)
    #print output

    print("Connecting to %s ... " % switch)

    remote_conn.send("terminal length 0\n")
    time.sleep(0.5)
    output = remote_conn.recv(1000)

    # Clear the Var.
    output = ""

    output = send_command("show run | inc hostname \n")

    for subline in output.splitlines():
        thisrow = subline.split()
        try:
            gotdata = thisrow[1]
            if thisrow[0] == "hostname":
                hostname = thisrow[1]
                prompt = hostname + "#"
        except IndexError:
            gotdata = 'null'

    # Write the output to a file (optional) - prepare file + filename before CMD loop
    if writeo:
        filetime = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
        filename = hostname + "-" + filetime + ".txt"
        filenames.append(filename)
        f = open(filename,'a')

    # Command Loop
    for cmd in commands:

        # Send the Command
        print switch + ": Running " + cmd
        output = send_command(cmd, prompt, bail_timeout)

        # Print the output (optional)
        if printo:
            print output
        if writeo:
            f.write(output)

    # /end Command Loop

    if writeo:
        # Close the File
        f.close()


    # Disconnect from SSH
    remote_conn_pre.close()

    if writeo:
        print("Switch %s done, output: %s" % (switch, filename))
    else:
        print("Switch %s done" % switch)

    # Sleep between SSH connections
    time.sleep(1)

print("\n")

print(" ********************************** ")
if writeo:
    print("  Output files: ")

    for ofile in filenames:
        print("   - %s" % ofile)

    print(" ---------------------------------- ")
print(" Script FINISHED ! ")
print(" ********************************** ")
