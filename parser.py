#!/usr/bin/env python3

##############################################################################
# Attempting to use python3 instead of 2.7.
#
# Open an OSSEC alert log, parse it, output to csv format.
#

# ######### IMPORTS #########
import os
import sys
import re
import json

# ######### VARIABLES #########
try:
    infile = sys.argv[1]
except:
    print('[-] ERROR: no file provided')
    exit()

ofile = 'alerts.json'

print('[*] reading %s') % infile

# ######### FUNCTIONS #########


# ########## MAIN PROGRAM #########
try:
    ifile = open(infile, 'r')
except IOError:
    print('[-] ERROR: unable to open file.')

#ofile = open(ofile, 'w')

# Read each line and display is relative parts
for line in ifile:
    '''
    This is messy but it works
    The first 3 lines should always be the same...
    Alert 1459569598.730897765: - syslog,sshd,invalid_login,authentication_failed,
    2016 Apr 01 23:59:58 (dns.sas.upenn.edu) 128.91.234.198->/var/log/secure
    Rule: 5710 (level 5) -> 'Attempt to login using a non-existent user'
    ----
    line 1: timestamp:- group array
    line 2: date time (hostname) ip_address->/path/to/log/file
    line 3: Rule id (level num) -> 'Description'
    ----
    We want the following fields
    - timestamp
    - groups
    - hostname
    - rule id
    - alert level
    - src ip (if available)
    - user (if available)
    - description
    '''

    # Patterns to match
    timestamp = re.compile('^\*\* Alert \d+.\d+')  # we want the number 10.9, xxxxxxxxxx.xxxxxxxxx
    hostname = re.compile('^201\d+ \w+ \d+ \d+:\d+:\d+ ')
    ruleid = re.compile('^Rule: \d+')  # iterate then grab alert level and description
    srcip = re.compile('^Src IP: \d+.\d+.\d+.\d+')
    user = re.compile('^User: \w+')

    linematched = 0

    # Test for matches. A line will have more than one matching RE.
    if timestamp.match(line):
        linematched = 1
        length = len(line)
        ts = ''
        i = 9
        while line[i] != ':':
            ts = ts + line[i]
            i += 1
        print('[*] ts: %s') % ts
        i = i + 4
        agroups = ''
        while i < length:
            agroups = agroups + line[i]
            i += 1
        print('[*] alert groups: %s') % agroups.strip()

    if hostname.match(line):
        linematched = 1
        i = 22
        hname = ''
        while line[i] != ')':
            if line[i] != '-':
                break
            hname = hname + line[i]
            i += 1
        print('[*] hostname: %s') % hname

    if ruleid.match(line):
        linematched = 1
        i = 6
        id = ''
        while line[i] != '(':
            id = id + line[i]
            i += 1
        i += 6
        print('[*] rule: %s') % id
        level = ''
        while line[i] != ')':
            level = level + line[i]
            i += 1
        print('[*] alert level: %s') % level
        description = ''
        ## add 6 to i after level
        i += 6
        while line[i] != "'":
            description = description + line[i]
            i += 1
        print('[*] description: %s') % description

    if srcip.match(line):
        linematched = 1
        length = len(line)
        i = 8
        src = ''
        while i < length:
            src = src + line[i]
            i += 1
        print('[*] srcip: %s') % src.strip()

    if user.match(line):
        linematched = 1
        length = len(line)
        i = 6
        username = ''
        while i < length:
            username = username + line[i]
            i += 1
        print('[*] username: %s') % username.strip()

    # We need to handle atomic (single log) and composite (multiple logs)
    # rules.
    #if linematched == 0:
    #    if len(line) > 1:
    #        # This must be the alert log line
    #        linematched = 1
    #        print('[*] alert log: %s') % line.strip()
    #        print('[ ]')
    print('[ ]')

# Try dumping the data read from ifile to JSON format.
#json.dump(ofile, ifile)

