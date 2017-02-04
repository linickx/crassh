#!/usr/bin/env python
# coding=utf-8

"""
    Nick Bettison

    Python script to test the crassh.py module (library)

    Run py.test for local code testing.
    Run py.test --cisco for testing code against a Cisco router (IOS Device)

"""

import os                       # ... standard Deps
import stat
import sys
import pytest                   # Pytest
import crassh                   # CraSSH!

# I don't care about long line, deal with it ;)
# pylint: disable=C0301
# the var err is assigned but not used on purpose
# pylint: disable=W0612

# Current Directory
CUR_DIR = os.path.dirname(__file__)

# Add Cisco testing option.
cisco = pytest.mark.skipif(
    not pytest.config.getoption("--cisco"),
    reason="need --cisco option to run Cisco IOS Tests"
)

"""
    Function / Code Tests - Self Contained.

    Naming Convention: Test_FunctionName.
"""

def test_help(tmpdir, capsys):
    """ This test is mainly used for syntax validation.
    If the help is printed and written to a text file then the script syntax is both Python 2 & Python 3.
    """
    with pytest.raises(SystemExit):
        crassh.print_help()
    out, err = capsys.readouterr()
    helpfile = tmpdir.mkdir("sub").join("help.txt")
    helpfile.write(out)
    assert helpfile.read() == out

def test_dnh_ok():
    """ Check that dnh doesn't trip on good commands
    """
    good_cmds = ["write mem"]
    for cmd in good_cmds:
        # if the function exists then we're in trouble and an assert will automagically be raised.
        crassh.do_no_harm(cmd)

def test_dnh_evil(capsys):
    """ Check for Evil things
    """
    evil_cmds = ["reload", "rel", "reload in 5", "write erase", "wr er", "del flash:/*", "delete system:running-config"]
    for cmd in evil_cmds:
        # If the function exits then that is good!
        with pytest.raises(SystemExit) as excinfo:
            crassh.do_no_harm(cmd)
            out, err = capsys.readouterr()
            print("\n *** Next/Failed Command: \"%s\" *** " % cmd)
        # https://pytest.org/latest/assert.html#assertions-about-expected-exceptions
        # print(excinfo.value)
        # The exit value must be 0
        assert str(excinfo.value) == "0"

def test_isgroupreadable(tmpdir):
    """ Check out file permission function works - Groups
    """
    test_groupfile = tmpdir.mkdir("sub").join("groupfile.txt")
    test_groupfile.write("text")
    os.chmod(str(test_groupfile), stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP) # Chmod 640
    assert crassh.isgroupreadable(str(test_groupfile)) is True

def test_isotherreadable(tmpdir):
    """ Check out file permission function works - others
    """
    test_othfile = tmpdir.mkdir("sub").join("otherfile.txt")
    test_othfile.write("text")
    os.chmod(str(test_othfile), stat.S_IRUSR | stat.S_IWUSR | stat.S_IROTH) # Chmod 604
    assert crassh.isotherreadable(str(test_othfile)) is True

def test_readtxtfile(tmpdir):
    """ Test that a text file is read and stripped correctly.
    """
    test_input = ["1.1.1.1", " 1.1.1.2", "1.1.1.3 ", " 1.1.1.4 "]
    ExpectedOutput = ["1.1.1.1", "1.1.1.2", "1.1.1.3", "1.1.1.4"]
    test_file = tmpdir.mkdir("sub").join("file.txt")
    f = open(str(test_file), 'a')
    for y in test_input:
        print(y)
        f.write(y + "\n")
    counter = 0
    Output = crassh.readtxtfile(str(test_file))
    for x in Output:
        assert x == ExpectedOutput[counter]
        counter += 1

def test_readauthfile(tmpdir):
    """ Test reading credentials from a file
    """
    test_file = tmpdir.mkdir("sub").join("credz.txt")
    f = open(str(test_file), 'a')
    f.write("[crassh] \n")
    f.write(" username = nick\n")
    f.write(" password =  pass  \n")
    f.close()
    os.chmod(str(test_file), stat.S_IRUSR | stat.S_IWUSR) # Chmod 600
    username, password = crassh.readauthfile(str(test_file))
    assert username == "nick"
    assert password == "pass"

"""
    Tests against a Cisco Switch, router, device, whatever!

    Naming Convention: Test_Cisco_FunctionName_x_y:
    * x = Function option, external reference (optional)
    * y = Multi (optional)
"""
@cisco
def test_cisco_main_shver_multi(capsys):
    """ Test Show ver (main function) against multiple devices
    """
    global sys
    SwitchFile = CUR_DIR + "/cisco_main_shver_multi_s.txt"         # IP Address of Switch/Router (for CLI Input)
    CmdFile = CUR_DIR + "/cisco_main_shver_multi_cmd.txt"          # The Command to run "show ver"
    OutputFile = CUR_DIR + "/cisco_main_shver_multi_output.txt"    # The expected output (from a "show ver")
    f = open(OutputFile, 'r')
    ExpectedOutput = f.readlines()
    sys.argv[1:] = ['-U', 'nick', '-P', 'nick', '-p', '-s', SwitchFile, '-c', CmdFile] # ./crassh -U nick -P nick -p -s SwitchFile -c CmdFile
    crassh.main()
    out, err = capsys.readouterr() # Capture output
    counter = 0
    for line in out.splitlines():
        #print("%s : %s" % (counter,line))
        assert ExpectedOutput[counter].strip() == line.strip()
        counter += 1

@cisco
def test_cisco_connect():
    """ Check that connection funtion returns expected hostname
    """
    device = "1.1.1.2"
    username = "nick"
    password = "nick"
    hostname = crassh.connect(device, username, password)
    crassh.disconnect()
    assert hostname == "r1"

@cisco
def test_cisco_connect_enable():
    """ Check that connection funtion returns expected hostname
    """
    device = "1.1.1.2"
    username = "cisco"
    password = "cisco"
    enable = True
    enable_password = "cisco123"
    hostname = crassh.connect(device, username, password, enable, enable_password)
    crassh.disconnect()
    assert hostname == "r1"

@cisco
def test_cisco_main_quit_default(capsys):
    """ Test main function quits properly against a failed router
    """
    global sys
    SwitchFile = CUR_DIR + "/cisco_main_quit_s.txt"                 # IP Address of Switch/Router (for CLI Input)
    CmdFile = CUR_DIR + "/cisco_main_shver_multi_cmd.txt"           # The Command to run "show ver"
    OutputFile = CUR_DIR + "/cisco_main_quit_default_output.txt"    # The expected output (from a "show ver")
    f = open(OutputFile, 'r')
    ExpectedOutput = f.readlines()
    sys.argv[1:] = ['-U', 'nick', '-P', 'nick', '-p', '-s', SwitchFile, '-c', CmdFile] # ./crassh -U nick -P nick -p -s SwitchFile -c CmdFile
    with pytest.raises(SystemExit):
        crassh.main()
    out, err = capsys.readouterr() # Capture output
    counter = 0
    for line in out.splitlines():
        assert ExpectedOutput[counter].strip() == line.strip()
        counter += 1

@cisco
def test_cisco_main_quit_disable(capsys):
    """ Test main function quit can be disabled (continue if router connection/authentication fails)
    """
    global sys
    SwitchFile = CUR_DIR + "/cisco_main_quit_s.txt"                 # IP Address of Switch/Router (for CLI Input)
    CmdFile = CUR_DIR + "/cisco_main_shver_multi_cmd.txt"           # The Command to run "show ver"
    OutputFile = CUR_DIR + "/cisco_main_quit_disable_output.txt"    # The expected output (from a "show ver")
    f = open(OutputFile, 'r')
    ExpectedOutput = f.readlines()
    sys.argv[1:] = ['-U', 'nick', '-P', 'nick', '-p', '-s', SwitchFile, '-c', CmdFile, '-Q'] # ./crassh -U nick -P nick -p -s SwitchFile -c CmdFile -Q
    crassh.main()
    out, err = capsys.readouterr() # Capture output
    counter = 0
    for line in out.splitlines():
        assert ExpectedOutput[counter].strip() == line.strip()
        counter += 1

@cisco
def test_cisco_main_backup(capsys):
    """ Test main function with backup credentials
    """
    global sys
    SwitchFile = CUR_DIR + "/cisco_main_backup_s.txt"           # IP Address of Switch/Router (for CLI Input)
    CmdFile = CUR_DIR + "/cisco_main_shver_multi_cmd.txt"       # The Command to run "show ver"
    OutputFile = CUR_DIR + "/cisco_main_backup_output.txt"      # The expected output (from a "show ver")
    f = open(OutputFile, 'r')
    ExpectedOutput = f.readlines()
    sys.argv[1:] = ['-U', 'fail', '-P', 'fail', '-B', 'nick', '-b', 'nick', '-p', '-s', SwitchFile, '-c', CmdFile] # ./crassh -U fail -P fail -B nick -b nick -p -s SwitchFile -c CmdFile
    crassh.main()
    out, err = capsys.readouterr() # Capture output
    counter = 0
    for line in out.splitlines():
        assert ExpectedOutput[counter].strip() == line.strip()
        counter += 1
