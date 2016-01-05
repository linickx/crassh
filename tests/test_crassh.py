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
