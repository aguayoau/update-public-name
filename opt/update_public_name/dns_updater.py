#!/usr/bin/python3 -u
import os
import json
import urllib3
import sys

ConfigurationFile = open(sys.argv[0] + '/inc/configuration.json', "r")
Configuration = json.loads(ConfigurationFile.read())
ConfigurationFile.close()

def dns_updater():
    http = urllib3.PoolManager()
    request = http.request('GET', 'http://ifconfig.co/json')
    CurrentData = json.loads(request.data.decode('utf-8'))
    if not(os.path.exists(Configuration['TemporaryPath']+"ip.tmpfile")) :
        print('File ' + Configuration['TemporaryPath']+ 'ip.tmpfile" doesn\'t exist. Creating the file')
        f = open(Configuration['TemporaryPath']+"ip.tmpfile", "w")
        f.write('{"ip":"0.0.0.0"}')

    f = open(Configuration['TemporaryPath']+"ip.tmpfile", "r+")
    OldData = json.loads(f.read())
    if CurrentData['ip'] != OldData['ip'] :
        print('Updating DNS record for ' + Configuration['PublicDNS'] + ' from ip ' + OldData['ip'] + ' to ' + CurrentData['ip'])
        f.seek(0)
        f.write(request.data.decode('utf-8'))
        request = http.request('GET', Configuration['UpdateURL'])
    else:
        print('DNS Record for ' + Configuration['PublicDNS'] + ' still the same')
    f.close()