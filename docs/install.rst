Installing C.R.A.SSH
####################

Crassh can be installed in two ways, either as a standalone script for users or via `pip` for developers.

Standalone installations are intended for Network Administrators

Developer installations are intended for those who want crassh imported into their own python scripts or wish the script to fall under package (*version*) management.

Standalone Installation
------------------------

You'll need both python and Paramiko_, once you have both of those just `download crassh.py direct from github`_ and save it somewhere ( *like* ``$HOME/bin`` ), e.g::

    curl -k -o crassh https://raw.githubusercontent.com/linickx/crassh/master/crassh.py
    chmod +x crassh

Developer (PIP) Installation
-----------------------------

Crassh has been published on PyPi: https://pypi.python.org/pypi/CraSSH

If your system supports pip (*with Internet access*) then crassh can be installed with:: 

    pip install crassh

The PIP installation will solve the dependencies and will make the command ``crassh`` available in your `$PATH` and make crassh available for ``import`` within your own python scripts.



Dependencies
------------

If you are not using ``pip`` then Paramiko will need to be manually installed:

Paramiko on Linux
^^^^^^^^^^^^^^^^^

For debian/ubuntu boxes::

   sudo apt-get install python-paramiko

For redhat/fedora boxes::

   sudo yum install python-paramiko

Paramiko on OS X
^^^^^^^^^^^^^^^^

For apples, get homebrew setup and then::

   brew install python  
   pip install paramiko

Paramiko on Windows
^^^^^^^^^^^^^^^^^^^

For windohz boxes, it's a bit more complicated.

* Download and install `Visual Studio C++ 2008 Express Edition`_ ( *do not install SQL* )
* Install `Python 2.7.8 – Select the correct MSI`_ for your architecture
* Download get-pip.py_ ( *Don’t use Internet Explorer it will mangle the file; _use Firefox_ to download.* )
* Open an **Administrator** command prompt and run:: 

    c:\Python27\python.exe get-pip.py

* From the same admin prompt, run:: 

    C:\Program Files\Microsoft Visual Studio 9.0\Common7\Tools\vsvars32.bat

* that's for 32bit machines… or for 64bit machines, run:: 
 
    C:\Program Files (x86)\Microsoft Visual Studio 9.0\Common7\Tools\vsvars64.bat

* From the same admin prompt, run:: 

    c:\Python27\Scripts\pip install paramiko

.. Links

.. _Paramiko: https://github.com/paramiko/paramiko
.. _`download crassh.py direct from github`: https://raw.githubusercontent.com/linickx/crassh/master/crassh.py
.. _`Visual Studio C++ 2008 Express Edition`: http://download.microsoft.com/download/A/5/4/A54BADB6-9C3F-478D-8657-93B3FC9FE62D/vcsetup.exe
.. _`Python 2.7.8 – Select the correct MSI`: https://www.python.org/download/releases/2.7.8/
.. _get-pip.py: https://bootstrap.pypa.io/get-pip.py

