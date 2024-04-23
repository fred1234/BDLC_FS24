# Setup on all Nodes

# Important

We need to modify the `/etc/hosts` file. It looks like an error from the deployment.

As user `student`, modify the `/etc/hosts` file

`sudo nano /etc/hosts`

The line with `127.0.1.1       bdlc-XX.labservices.ch bdlc-XX` is wrong and you should delete it.

e.g. from:

```bash

127.0.0.1 localhost

127.0.1.1       bdlc-18.labservices.ch bdlc-18

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
wget https://downloads.apache.org/hadoop/common/hadoop-3.3.4/hadoop-3.3.4.tar.gz
tar -xvzf hadoop-3.3.4.tar.gz
mv hadoop-3.3.4 hadoop

echo "Spark"
wget https://dlcdn.apache.org/spark/spark-3.3.2/spark-3.3.2-bin-hadoop3.tgz
tar xvf spark-3.3.2-bin-hadoop3.tgz
mv spark-3.3.2-bin-hadoop3 spark

```
