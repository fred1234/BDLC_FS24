# How to go back to single cluster mode (after project work)

Log in to your _master_ node and switch to user `cluster`.

Stopping all services:

```bash
stop-all.sh
stop-dfs.sh
~/spark/sbin/stop-all.sh
stop-history-server.sh
```

Stopping `Jupyter Lab`:

```bash
ps -ef | grep jupyter
```

e.g output like:

```text
hadoop    152556  152476  6 11:06 pts/0    00:00:01 /usr/bin/python3 /home/hadoop/.local/bin/jupyter-lab
```

Then kill the process with:

```bash
kill 152556
```

## Your Machine

Connect to your machine now. Check again that `jps` does not return anything, otherwise kill it.

Change the user to `hadoop`:

```bash
student@bdlc-19:~$ su - hadoop
Password:
hadoop@bdlc-19:~$
```

Make sure that you have enough disk space.

```bash
hadoop@bdlc-19:~$ df -h
Filesystem                         Size  Used Avail Use% Mounted on
/dev/mapper/ubuntu--vg-ubuntu--lv   49G   21G   26G  46% /
/dev/sdb                           147G   40G  100G  29% /data
hadoop@bdlc-19:~$
```

### Not enough disk space

If not. Delete data. If you are short on `/data`

```bash
rm -rf /data/hdfscluster/
```

And similarly, if you are short on `/`, delete the user `cluster` (has to be executed as `student`)

```bash
sudo userdel -r cluster
```

### Starting Services

```bash
start-all.sh
mr-jobhistory-daemon.sh start historyserver
nohup hive --service metastore > metastore.log &
nohup hive --service hiveserver2 > hiveserver.log &
nohup jupyter lab > error.log &
start-history-server.sh
```

Wait a minute...

The services should be up and running again

- http://bdlc-XX.labservices.ch:9870/dfshealth.html#tab-overview
- http://bdlc-XX.labservices.ch:18080/
- http://bdlc-XX.labservices.ch:10002/
- http://bdlc-XX.labservices.ch:8888/lab?
