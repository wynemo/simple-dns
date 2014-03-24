introduction
------------

so, just reinvent a wheel like dnscrypt


configuration
-------------

change **server-ip** in config.json to your remote server ip

on your remote server run::

    python -B udp-server.py

on your local machine run::

    python -B udp-client.py


win7 set localhost dns
----------------------

::

    netsh interface ipv4 set dnsservers "Wireless Network Connection" static 127.0.0.1

python 3
--------

::

    2to3 -w *.py
