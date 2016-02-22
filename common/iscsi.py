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
    
    def discover(self, ip, prot=3260):
        # # iscsiadm -m discovery -t sendtargets -p <portalip>
        return True
    
    def login(self, iqn):
        # # iscsiadm -m node --targetname=<targetname> --login
        return True
        
    def logout(self, iqn):
        # # iscsiadm -m node --targetname=<targetname> --logout
        return True
    
    def getDevByName(self, iqn, ip, port=3260, lun=0):
        path='/dev/disk/by-path/ip-'+ip+':'+str(port)+'-iscsi-'+iqn+'-lun-'+str(lun)
        for l in glob.glob(path):
            print(os.path.realpath(l))
