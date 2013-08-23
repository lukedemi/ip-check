import socket
import urllib
import logging

logfile = "/var/log/dnscheck.log"
ipfile = "/var/spool/ipaddr"
apifile = "/etc/api_url"
service = "http://icanhazip.com/"

def fileExists(filename):
    try:
        with open(filename): pass
    except IOError:
        print '%s does not exist. Exiting.' % (filename)
        exit(1)

fileExists(logfile)
fileExists(ipfile)
fileExists(apifile)

a = open(apifile, 'r')
apiurl = a.read().strip()
a.close()

logging.basicConfig(format='%(asctime)s %(message)s',filename=logfile,level=logging.DEBUG)

ip = urllib.urlopen(service).read().strip()

f = open(ipfile, 'r+')
c_ip = f.read().strip()

if ip == c_ip:
    logging.info('All Gravy: %s = %s' % (ip, c_ip))
else:
    try:
        socket.inet_aton(ip)
    except socket.error:
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
