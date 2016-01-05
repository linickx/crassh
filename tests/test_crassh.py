#!/usr/bin/env python
import crassh
import os, pytest


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
    evil_cmds = ["reload", "reload in 5", "write erase", "wr er", "del flash:/*", "delete system:running-config"]
    for cmd in evil_cmds:
        # If the function exits then that is good!
        with pytest.raises(SystemExit) as excinfo:
            crassh.do_no_harm(cmd)
        # https://pytest.org/latest/assert.html#assertions-about-expected-exceptions
        # print(excinfo.value)
        # The exit value must be 0
        assert str(excinfo.value) == "0"
