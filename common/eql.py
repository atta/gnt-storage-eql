# disable eventlog to make parsing possible
# cli-settings events on|off

import paramiko
import time
import sys
import re

class eql(object):
    '''
    exec eql commands
    '''
    enviroment=None

    eql_ip=None
    eql_name=None
    eql_user=None
    eql_pass=None
 
    ssh=None
    chan=None
    
    def __init__(self, name, ip, user, password):
        self.eql_ip = ip
        self.eql_name = name
        self.eql_user = user
        self.eql_pass = password
    
    def connect(self):
        # open the connection an set some cli-settings
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy( paramiko.AutoAddPolicy() )
        self.ssh.connect(self.eql_ip, username=self.eql_user, password=self.eql_pass)
        self.chan = self.ssh.invoke_shell()
        self.run_cmd('cli-settings formatoutput off')
        self.run_cmd('cli-settings paging off')
        self.run_cmd('cli-settings displayinMB on')
        self.run_cmd('cli-settings confirmation off')
    
    def close(self):
        # set the cli-settings back and close the ssh session
        self.run_cmd('cli-settings formatoutput on')
        self.run_cmd('cli-settings paging on')
        self.run_cmd('cli-settings displayinMB off')
        self.run_cmd('cli-settings confirmation on')
        self.ssh.close()
        
    def run_cmd(self, cmd):
        buff = ''
    
        # wait for promt.
        while not buff.endswith(self.eql_name+'> '):
            self.chan.send('\r\n')
            time.sleep(0.1)
            resp = self.chan.recv(900)
            buff += resp.decode("utf-8") 
        
        # send cmd
        if buff.endswith(self.eql_name+'> '):
            buff = ''
            self.chan.send(cmd+'\r\n')
        
        # read output
        while not buff.endswith(self.eql_name+'> '):
            time.sleep(0.5)
            resp = self.chan.recv(9000)
            buff += resp.decode("utf-8")
            # split output remove command and prompt 
            return str(resp)[len(cmd+'\r\n'):(len('\r\n'+self.eql_name+'> '))*-1].split('\r\n')
    
    def whoami (self):
        # a easy test do nothing bad
        return self.run_cmd('whoami')[0]

    def volCreate(self, name, size):
        # size in MB, access is done in an extra task
        data = self.run_cmd('volume create gnt-'+name+' '+str(size)+'MB description gnt-'+name+' read-write online iscsi-alias gnt-'+name+' thin-provision')
        result = self.volShow(name)
        if result != None and result['Name'] == 'gnt-'+name:
            return name
            
        return ''.join(data)
    
    def volGrow(self, name, size):
        # set the new size absolute in MB
        data = self.run_cmd('volume select gnt-'+name+' size '+str(size))
        
    def volDelete(self, name):
        # get rid of a volume, handle with care can not be reverted
        self.run_cmd('volume select gnt-'+name+' offline')
        self.run_cmd('volume delete gnt-'+name)

    def volSetAccess(self, name, ip = '*.*.*.*', initiatorname='*'):
        # add ACL to a Volume, get a list of all Volume Access-Slots and add it not exists
        for number in self.volGetAccessList(name):
            access = self.volGetAccess(name, number)
            if access != None and access['Initiator'] == initiatorname and access['IPAddress'] == ip:
                return True
            
        self.run_cmd('volume select gnt-'+name+' access create ipaddress '+ip+' initiator '+initiatorname)
        self.run_cmd('volume select gnt-'+name+' multihost-access enable')
  
    def volGetAccessList(self, name):
        # grep all used ACL-slot numbers and return it as array of slot-numbers
        data=[]
        pattern = re.compile("^[0-9]+\s.*$")
        for info in self.run_cmd('volume select gnt-'+name+' access show')[6:]:
            if pattern.match(info):
                data.append(int(info.split()[0]))
        return data
    
    def volGetAccess(self, name, number):
        # Get ACL-Settings from a slot
        data={}
        val=''
        key=''
        for info in self.run_cmd('volume select gnt-'+name+' access select '+str(number)+' show'):
            #drop lines with useless informations
            if info.startswith('--'):
                continue
            if info.startswith('__'):
                continue
            if ': ' in info:
                key, val = info.split(': ')
                data[key]=val
            else:
                if data.has_key(key):
                    data[key]=data[key]+info
        if len(data) == 0:
            return None
        return data
    
    def volShow(self, name):
        # retrive volume informations
        data={}
        val=''
        key=''
        for info in self.run_cmd('volume show gnt-'+name):
            #drop lines with useless informations
            if info.startswith('--'):
                continue
            if info.startswith('__'):
                continue
            if info.startswith('ID '):
                continue
            if info.startswith(' '):
                continue
            if re.search('^[0-9]+\s+\w',info):
                continue
            if info.startswith('Access Policy Group'):
                continue

            if ': ' in info:
                key, val = info.split(': ')
                data[key]=val
            else:
                if data.has_key(key):
                    data[key]=data[key]+info
        if len(data) == 0:
            return None
        return data
        