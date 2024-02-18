# Installation of Apache Hadoop in Standalone Operation

> By default, Hadoop is configured to run in a non-distributed mode, as a single Java process. This is useful for debugging.

We will use the official installation documentation from [Apache Hadoop](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/SingleCluster.html)

## SSH

SSH into your machine with `ssh student@bdlc-XX.labservices.ch`, where `XX` is your personal virtual machine number.

## Update and Upgrade your Software

Before we start, let's upgrade the software

```bash
sudo apt update
# answer with Y on: Do you want to continue? [Y/n] Y
sudo apt upgrade
```

## Hadoop User

We will create a user `hadoop` and won't use our `student` account. All Hadoop processes will run under the user `hadoop`.

```bash
# create a new user called 'hadoop'
# give it a new password (and also remember it ;)) and confirm with Y

sudo adduser hadoop
```

The command `sudo adduser hadoop` will look like:

```bash
# [sudo] password for student:
# Adding user `hadoop' ...
# Adding new group `hadoop' (1004) ...
# Adding new user `hadoop' (1004) with group `hadoop' ...
# Creating home directory `/home/hadoop' ...
# Copying files from `/etc/skel' ...
# New password:
# Retype new password:
# passwd: password updated successfully
# Changing the user information for hadoop
# Enter the new value, or press ENTER for the default
# 	Full Name []: Hadoop User
# 	Room Number []:
# 	Work Phone []:
# 	Home Phone []:
# 	Other []:
# Is the information correct? [Y/n] Y
```

## Java

I have already preinstalled the correct java version. In other words, you don't have to take care about the java version. For reference, I did:

```bash
sudo apt install openjdk-11-jdk
```

To verify that we have indeed the version `11.0.21`, run:

```bash
java --version
```

## Following the Apache Hadoop Guide

If not done already, open the official [installation guide](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/SingleCluster.html).

```bash
# install pdsh
# answer with Y on: Do you want to continue? [Y/n] Y
sudo apt-get install pdsh
```

Now, we will switch to this user. All following steps should be executed as user `hadoop`.

```bash
# switch to the user hadoop
su - hadoop

# change to the home directory
cd ~

# verify "who you are" with
whoami
```

```bash
# download the latest hadoop distribution
wget https://dlcdn.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz

# check with ls that the file is around
# you should see: hadoop-3.3.6.tar.gz
ls

# extract hadoop-3.3.6.tar.gz
tar -xvzf hadoop-3.3.6.tar.gz

# check again with ls if you see the folder hadoop-3.3.6
ls

# rename the folder to hadoop
mv hadoop-3.3.6 hadoop
```

We need to specify `JAVA_HOME` in `~/hadoop/etc/hadoop/hadoop-env.sh`. To figure out where java's home is, run:

```bash
dirname $(dirname $(readlink -f $(which java)))
```

and copy the output (`/usr/lib/jvm/java-11-openjdk-amd64`).

```text
change the line from
# export JAVA_HOME=
```

to

```text
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
```

with

```bash
nano ~/hadoop/etc/hadoop/hadoop-env.sh
```

## Run Apache Hadoop in Standalone Operation

Let's start to run Hadoop. Check if we get the usage help when we type `~/hadoop/bin/hadoop`. Note, it should execute without an error.

```bash
~/hadoop/bin/hadoop

# should give you the usage help..
#
# Usage: hadoop [OPTIONS] SUBCOMMAND [SUBCOMMAND OPTIONS]
#  or    hadoop [OPTIONS] CLASSNAME [CLASSNAME OPTIONS]
#   where CLASSNAME is a user-provided Java class
# ...
```

:sparkles: congrats :sparkles: - you finished the standalone operation installation.

## Examples

Try to run the example provided in the documentation.

```bash
mkdir ~/input
cp ~/hadoop/etc/hadoop/*.xml ~/input
ls -al ~/input

~/hadoop/bin/hadoop jar ~/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar grep ~/input ~/output 'dfs[a-z.]+'
```

Can you explain what the program does?

## Homework

Check the [Homework](./v01_exercises.md)

## References

- [Hadoop - Single Cluster](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/SingleCluster.html)
- [Tutorial - Hadoop on Single Node](https://tecadmin.net/install-hadoop-on-ubuntu-20-04/)
- [Tutorial - Hadoop on Multi Node](https://medium.com/@jootorres_11979/how-to-set-up-a-hadoop-3-2-1-multi-node-cluster-on-ubuntu-18-04-2-nodes-567ca44a3b12)
