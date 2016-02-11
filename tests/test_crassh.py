#!/usr/bin/env python
import crassh
import os, pytest, stat, sys

CUR_DIR = os.path.dirname(__file__)
#TEST_DIR = os.path.join(CUR_DIR, 'tests')

cisco = pytest.mark.skipif(
    not pytest.config.getoption("--cisco"),
    reason="need --cisco option to run Cisco IOS Tests"
)

def test_help(tmpdir, capsys):
    # This test is mainly used for syntax validation. If the help is printed and written to a text file then the script syntax is both Python 2 & Python 3.
    with pytest.raises(SystemExit):
        crassh.print_help()
    out, err = capsys.readouterr()
    helpfile = tmpdir.mkdir("sub").join("help.txt")
    helpfile.write(out)
    assert helpfile.read() == out

def test_dnh_ok():
    # Check that dnh doesn't trip on good commands
    good_cmds = ["write mem"]
    for cmd in good_cmds:
        # if the function exists then we're in trouble and an assert will automagically be raised.
        crassh.do_no_harm(cmd)

def test_dnh_evil(capsys):
    # Check for Evil things
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
    # Check out file permission function works - Groups
    test_groupfile = tmpdir.mkdir("sub").join("groupfile.txt")
    test_groupfile.write("text")
    os.chmod(str(test_groupfile), stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP)
    assert crassh.isgroupreadable(str(test_groupfile)) == True
    
def test_isotherreadable(tmpdir):
    # Check out file permission function works - others 
    test_othfile = tmpdir.mkdir("sub").join("otherfile.txt")
    test_othfile.write("text")
    os.chmod(str(test_othfile), stat.S_IRUSR | stat.S_IWUSR | stat.S_IROTH)
    assert crassh.isotherreadable(str(test_othfile)) == True
    
@cisco
def test_cisco_main_shver(capsys):
    global sys
    SwitchFile = CUR_DIR + "/cisco_shver_s.txt"
    CmdFile = CUR_DIR + "/cisco_shver_cmd.txt"
    OutputFile = CUR_DIR + "/cisco_shver_output.txt"
    f=open(OutputFile,'r')
    ExpectedOutput = f.readlines()
    #ExpectedOutput = f.read()
    sys.argv[1:] = ['-U', 'nick', '-P', 'nick', '-p', '-s', SwitchFile, '-c', CmdFile]
    crassh.main()
    out, err = capsys.readouterr()
    counter = 0
    for line in out.splitlines():
        #print("%s : %s" % (counter,line))
        assert ExpectedOutput[counter].strip() == line.strip()
        counter += 1

@cisco
def test_cisco_connect():
    # Check that connection funtion returns expected hostname

    device = "1.1.1.2"
    username = "nick"
    password = "nick"
    enable = ""

    hostname = crassh.connect(device, username, password, enable)
    
    assert hostname == "r1"