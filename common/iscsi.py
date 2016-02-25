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
import re

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
            sys.stdout.write("%s" % line)
        return True
    
    def login(self, iqn):
        cmd='iscsiadm -m node --targetname='+iqn+' --login'
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            sys.stdout.write("%s" % line)
        return True
        
    def logout(self, iqn):
        cmd='iscsiadm -m node --targetname='+iqn+' --logout'
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            sys.stdout.write("%s" % line)
        return True
    
    def getMultipathDev(self, iqn, ip, port=3260, lun=0):
        # grep for the scsi_id in the multipath-output and return the devicemapper name dm-<n>
        cmd = 'multipath -ll | grep $(/lib/udev/scsi_id -g /dev/disk/by-path/ip-'+ip+':'+str(port)+'-iscsi-'+iqn+'-lun-'+str(lun)+')'
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        result = re.search('\sdm-\d+\s',process.stdout.readlines()[0])
        dm = ''.join(['/dev/', result.group().strip()])
        if '/dev/dm-' in dm:
            return dm
        return None
