introduction
------------

a very simple and stupid DNS server to bypass the DNS pollution.
很傻的DNS server，破DNS污染。


how it works:
-------------

your remote server listen on a port other than 53, (as you can see in `config.json.remote`, it's 60053).
你远程DNS服务器监听的端口不是53。


configuration
-------------

change **remote_ip** in config.json.local to your remote server ip 改一下这个字段

on your remote server run, 远程机器::

    python dns-client.py config.json.remote

on your local machine run, 本机::

    python dns-client.py config.json.local
    
test
----

::

    nslookup google.com 127.0.0.1


win7 set localhost dns
----------------------

::

    netsh interface ipv4 set dnsservers "Wireless Network Connection" static 127.0.0.1

