ip-check
========

This is a script I wrote in python to check the external IP address of my server every five minutes to see if it has changed. If so, it uses the api of my dns provider to change my DNS A record. It's more or less a dyndns alternative.

You're going to need to create a couple files in order for this script to work.

/var/log/dnscheck.log = logging output for debug/info
/var/spool/ipaddr = stores the current ip address
/etc/api_url = the url to request if the IP address does change.
