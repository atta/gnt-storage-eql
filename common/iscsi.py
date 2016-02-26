# Target discovery
# # iscsiadm -m discovery -t sendtargets -p <portalip>
# Delete obsolete targets
# # iscsiadm -m discovery -p <portalip> -o delete
# Login to available targets
# # iscsiadm -m node -L all
# or login to specific target
# # iscsiadm -m node --targetname=<targetname> --login
# logout:
# # iscsiadm -m node -U all

# Info for running session
# # iscsiadm -m session -P 3
# The last line of the above command will show the name of the attached dev e.g
# Attached scsi disk sdd State: running
# For the known nodes
# # iscsiadm -m node

import subprocess
import sys
import os
import re
import time

class iSCSI(object):
    
    def __init__(self):
        pass
    
    def getInitiatorname(self, file='/etc/iscsi/initiatorname.iscsi'):
        txt = open(file, 'r')
        initiatorname = ''
        for line in txt.read().split('\n'):
            line=line.strip()
            if line.startswith('InitiatorName='):
                initiatorname = line.split('=')[1].strip()
        return initiatorname 
    
    def discover(self, ip, port=3260):
        cmd = 'iscsiadm -m discovery -t st -p '+ip+':'+str(port)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            sys.stderr.write("%s" % line)
        return True
    
    def login(self, iqn):
        cmd='iscsiadm -m node --targetname='+iqn+' --login'
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            sys.stderr.write("%s" % line)
        return True
        
    def logout(self, iqn):
        cmd='iscsiadm -m node --targetname='+iqn+' --logout'
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            sys.stderr.write("%s" % line)
        return True
    
    def getMultipathDev(self, iqn, ip, port=3260, lun=0):
        # wait for link
        path='/dev/disk/by-path/ip-'+ip+':'+str(port)+'-iscsi-'+iqn+'-lun-'+str(lun)
        while not os.path.islink(path):
            sys.stderr.write("path not found %s" % path)
            time.sleep(0.2)
        
        cmd = '/lib/udev/scsi_id -g '+path
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        scsi_id = process.stdout.readlines()[0]
        
        # grep for the scsi_id in the multipath-output and return the devicemapper name dm-<n>
        cmd = 'multipath -ll | grep -o -e "'+scsi_id+'.*dm-[[:digit:]]\+"'
        
        dm = ''
        while dm == '': 
            try:
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                result = re.search('\sdm-\d+',process.stdout.readlines()[0])
                dm = ''.join(['/dev/', result.group().strip()])
            except:
                sys.stderr.write("scsi_id %s no found in multipath" % scsi_id)
                time.sleep(1)
            
        if '/dev/dm-' in dm:
            return dm
        return None
