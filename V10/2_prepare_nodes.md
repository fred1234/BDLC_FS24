# Setup on all Nodes

# Important

We need to modify the `/etc/hosts` file.

As user `student`, modify the `/etc/hosts` file

`sudo nano /etc/hosts`

e.g. from:

```bash
127.0.0.1       bdlc-XX.labservices.ch bdlc-XX localhost

# The following lines are desirable for IPv6 capable hosts
::1     ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
```

to:

```bash

127.0.0.1 localhost

# The following lines are desirable for IPv6 capable hosts
::1     ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
```

We also need to change the dns suffix.

```bash
sudo vim /etc/netplan/50-cloud-init.yaml
```

e.g. from:

```bash
# This file is generated from information provided by the datasource.  Changes
# to it will not persist across an instance reboot.  To disable cloud-init's
# network configuration capabilities, write a file
# /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg with the following:
# network: {config: disabled}
network:
    version: 2
    ethernets:
        eth0:
            addresses:
            - 10.164.150.116/24
            match:
                macaddress: bc:24:11:67:d3:4d
            nameservers:
                addresses:
                - 1.1.1.1
                search:
                - ls.eee.intern
            routes:
            -   to: default
                via: 10.164.150.254
            set-name: eth0
```

to:

```bash
# This file is generated from information provided by the datasource.  Changes
# to it will not persist across an instance reboot.  To disable cloud-init's
# network configuration capabilities, write a file
# /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg with the following:
# network: {config: disabled}
network:
    version: 2
    ethernets:
        eth0:
            addresses:
            - 10.164.150.116/24
            match:
                macaddress: bc:24:11:67:d3:4d
            nameservers:
                addresses:
                - 1.1.1.1
                search:
                - labservices.ch
            routes:
            -   to: default
                via: 10.164.150.254
            set-name: eth0
```

Apply the changes with:

```bash
sudo netplan apply
```

And see if you can ping bdlc-16:

```bash
ping bdlc-16
PING bdlc-16.labservices.ch (10.164.150.116) 56(84) bytes of data.
64 bytes from 10.164.150.116 (10.164.150.116): icmp_seq=1 ttl=64 time=1.24 ms
^C # stop it with ctrl+c
```



## User

We are going to create a new user for the cluster setup. This user will be used for your project work.

As user `student`.

```bash
sudo adduser cluster
```

## Namenode & Datanode Directories

```bash
sudo mkdir -p /data/hdfscluster/namenode
sudo mkdir -p /data/hdfscluster/datanode
```

and give the `cluster` user the access rights to the folders:

```bash
sudo chown cluster:root -R /data/hdfscluster/
```

## TMP Directory for Spark
```bash
sudo mkdir /data/tmpcluster
sudo chown cluster:root -R /data/tmpcluster/
```

## Switching the User

Now, we will switch to this user. All following steps should be executed as user `cluster`.

```bash
# switch to the user cluster
su - cluster

# change to the home directory
cd ~

# verify "who you are" with
whoami
```

## Hadoop & Spark

Download Hadoop and Spark, extract it and rename.

```bash
cd ~

echo "Hadoop"
wget https://dlcdn.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz
tar -xvzf hadoop-3.3.6.tar.gz
mv hadoop-3.3.6 hadoop


echo "Spark"
wget https://dlcdn.apache.org/spark/spark-3.5.1/spark-3.5.1-bin-hadoop3.tgz
tar xvf spark-3.5.1-bin-hadoop3.tgz
mv spark-3.5.1-bin-hadoop3 spark

```
