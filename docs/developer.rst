Developer Guide
###############

Crassh is supplied as a Python module which developers can include in their own scripts. Crassh is a Paramiko wrapper specifically designed for talking to Cisco IOS devices and routers.

Developers/Coders are reminded not to *reinvent the wheel*, crassh (*as a standalone script*) can already read commands from a file and execute them on either one device or many devices (*i.e. read list of devices from a file*), tasks such as backing up the network estate do not require any additional scripts/development.

Where crassh *as a module* is valuable is doing *something* other than executing commands and printing/storing the result. 

An example of *doing something* is writing an auditing script; the `following example`_ is taken from my `personal blog`_ where crassh can be used in a script to look for the *insecure* SNMP community ``public``. ::

    #!/usr/bin/env python
    # coding=utf-8

    import crassh

    # Variables
    routers = ["10.159.83.135", "10.159.83.136"]
    username = "nick"
    password = "nick"

    # Loop
    for device in routers:

        hostname = crassh.connect(device, username, password)
        output = crassh.send_command("show run | inc snmp-server community", hostname)
        crassh.disconnect()

        # Split the output by spaces so we can search the response
        words = output.split()

        # Look for "public" in the output
        for x in words:
            if x == "public":
                print("DANGER: Public SNMP Community set on %s [%s]" % (hostname, device))



C.R.A.SSH (crassh) autodoc
--------------------------

The *autodoc* automagically documents all of the functions from the `source code`_.

.. automodule:: crassh
    :members:


.. Links
.. _`personal blog`: http://www.linickx.com
.. _`following example`: http://www.linickx.com/pip-install-crassh
.. _`source code`: https://github.com/linickx/crassh/