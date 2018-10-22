import sys
import os

import nmap
import time
import threading

# Configuration
SCAN_NETWORK=   '127.0.0.1'
SCAN_PORTNUM=   '22-443'
SCAN_PERIOD =   '5'
SCAN_OUTPUT =   'data/scan.csv'

# Initialize NMAP
try:
    nm = nmap.PortScanner()         # instantiate nmap.PortScanner object
except nmap.PortScannerError:
    print('Nmap not found', sys.exc_info()[0])
    sys.exit(1)
except:
    print("Unexpected error:", sys.exc_info()[0])
    sys.exit(1)


def start_scan():
    nm.scan(SCAN_NETWORK, SCAN_PORTNUM)
    
    # Writes to stdout
    display_hosts(nm)

    # Write to CSV file
    export_scan_csv(nm)

    # Restart the scan every 5 seconds
    threading.Timer(5, start_scan).start()



### Display functions ###
def display_hosts(nm):
    for host in nm.all_hosts():
        print('----------------------------------------------------')
        print('Host : %s (%s)' % (host, nm[host].hostname()))
        print('State : %s' % nm[host].state())
        for proto in nm[host].all_protocols():
            print('----------')
            print('Protocol : %s' % proto)

            lport = nm[host][proto].keys()
            lport.sort()
            for port in lport:
                print ('port : %s\tstate : %s' % (port, nm[host][proto][port]['product']))

def export_scan_csv(nm):
    stdout = sys.stdout
    sys.stdout = open(SCAN_OUTPUT, 'w')

    print('IP, Hostname, Protocol, Port, Product, Version')
    for host in nm.all_hosts():
        for proto in nm[host].all_protocols():
            lport = nm[host][proto].keys()
            lport.sort()
            for port in lport:
                hostname    = nm[host].hostname()
                product     = nm[host][proto][port]['product']
                version     = nm[host][proto][port]['version']
                entry = host + ', ' + hostname + ', ' + proto + ', ' + str(port) + ', ' + product + ', ' + version
                print(entry)
    sys.stdout = stdout

### Program start ###
start_scan()