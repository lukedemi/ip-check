import socket
import urllib
import logging

# Location for the program to output logs
logfile = "/var/log/dnscheck.log"
# Where the "current" IP address is stored.
ipfile = "/var/spool/ipaddr"
# File containing the URL used to update DNS
apifile = "/etc/api_url"
# Service to check external IP. There are several if you google.
service = "http://icanhazip.com/"

def fileExists(filename):
    try:
        with open(filename): pass
    except IOError:
        print '%s does not exist. Touch it.' % (filename)
        exit(1)

fileExists(logfile)
fileExists(ipfile)
fileExists(apifile)

# Cleans up apiurl and sets it to a variable
a = open(apifile, 'r')
apiurl = a.read().strip()
a.close()

# Sets logging format
logging.basicConfig(format='%(asctime)s %(message)s',filename=logfile,level=logging.DEBUG)

ip = urllib.urlopen(service).read().strip()

# Sets the current IP to be the IP one delivered by the IP service
f = open(ipfile, 'r+')
c_ip = f.read().strip()

if ip == c_ip:
    # If all's good, carry on
    logging.info('All Gravy: %s = %s' % (ip, c_ip))
else:
    try:
        socket.inet_aton(ip)
    except socket.error:
        # Making sure we aren't getting a "service unavailable" or similar
        logging.error("Response '%s' recieved from service '%s' does not seem to be valid. Exiting." \
                     % (ip, service))
        exit(1) 
    logging.info("NO MATCH: %s != %s. File /var/spool/ipaddr changed to %s" % (ip, c_ip, c_ip))
    output = urllib.urlopen(apiurl).read()
    logging.info(output)
    f.seek(0)
    f.write("%s" % (ip))
    f.truncate()
    f.close
