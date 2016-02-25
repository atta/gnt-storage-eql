#!/usr/bin/env python2
#
# Copyright (C) 2016
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

# Based on Ganeti EXtStorageProviders code (https://code.grnet.gr/projects/extstorage)

"""Read config to manage Volumes in Dell Equallogic 

#### description ####
# * storage_net: is the Network the Client connects from, your SAN
# * storage_ip: Master-IP of your Equallogic Cluster
# * storage_port: iSCSI port default is 3260

example configuration:

  [default]
  device_hostname=eql01
  management_ip=192.168.2.245
  management_user=admin
  management_password=calvin
  storage_net=*.*.*.*
  storage_ip=192.168.1.100
  storage_port=3260

Rise parse error if config fails
"""
import ConfigParser

class config(object):
    '''
    classdocs
    '''

    def __init__(self,filename='/etc/ganeti/extstorage/eql.conf'):
        '''
        Constructor
        '''
        self.config = ConfigParser.SafeConfigParser()
        if not self.config.read(filename):
            raise ConfigParser.Error("Unable to read config file")
        
        self.device_hostname=self.config.get('default', 'device_hostname')
        self.management_ip=self.config.get('default', 'management_ip')
        self.management_user=self.config.get('default', 'management_user')
        self.management_password=self.config.get('default', 'management_password')
        self.storage_net=self.config.get('default', 'storage_net')
        self.storage_ip=self.config.get('default', 'storage_ip')
        self.storage_port=self.config.get('default', 'storage_port')
