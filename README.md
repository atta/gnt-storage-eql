# Ganeti ext-storage interface for Dell Equallogic

more information can be found at: [http://docs.ganeti.org/ganeti/master/html/man-ganeti-extstorage-interface.html]

## requirements

This interfase is tested in an Ubuntu 14.04 environment, packages need to be installed on the node:

### Software
* open-iscsi
* multipath-tools
* python-paramiko

### SAN interface setting
```
  auto san1
  iface san1 inet static
      mtu 9000
      address 192.168.a.b
      netmask 255.255.255.0
      pre-up sysctl -w net.ipv4.conf.san1.rp_filter=2
      post-up iscsiadm -m iface -I san1 -o new && iscsiadm -m iface -I san1 --op=update -n iface.net_ifacename -v san1
```

### multipath configuration
```
  defaults {
          user_friendly_names no 
          path_grouping_policy multibus
          polling_interval 3
          path_selector "round-robin 0"
          failback immediate
          features "0"
          no_path_retry 1
  }
  
  blacklist {
      devnode "^(ram|raw|loop|fd|md|dm-|sr|scd|st)[0-9]*"
      devnode "^(hd|xvd|vd)[a-z][[0-9]*]"
      #devnode "^(sd)[a-b][[0-9]*]"
      devnode "^cciss!c[0-9]d[0-9]*[p[0-9]*]"
  }
  
  devices {
      device {
          vendor          "EQLOGIC"
          product         "100E-00"
              path_grouping_policy multibus
              path_selector "round-robin 0"
              failback immediate
              features "0"
              no_path_retry 1
      }
  }
  
  multipaths {
      multipath {
          wwid    *
      }
  }
```

## Equallogic CLI

### connect to SSH
At the connect step some settings are done to make parsing possible
```
  # disable system events shown in the CLI
  cli-settings events off
  
  # do not ask for non reversible commands to confirm
  cli-settings confirmation off
  
  # one information per line
  cli-settings formatoutput off
  
  # print all
  cli-settings paging off
  
  # use MB as unit
  cli-settings displayinMB on
```

### create Volume
```
  volume create <NAME> <SIZE>MB description gnt-<NAME> read-write online iscsi-alias gnt-<NAME> thin-provision
```

### grant Access to a Volume
```
  volume select gnt-'+name+' access create ipaddress *.*.*.* initiator *
```

### show Volume
```
  volume show <NAME>
```

### delete Volume
```
  volume select <NAME> offline
  volume delete <NAME> 
```

### grow Volume
SIZE is the new absolute Volumesize in MB
```
  volume select gnt-<NAME> size <SIZE>
```

