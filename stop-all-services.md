# Shutdown all Services

```bash
stop-all.sh
mr-jobhistory-daemon.sh stop historyserver
stop-history-server.sh
```

Kill these services with `kill pid`

```bash
ps -ef | grep metastore
ps -ef | grep hiveserver2
ps -ef | grep jupyter
```

## Verification

Check with `jps` on each node.

```bash
ps -ef | grep metastore
ps -ef | grep hiveserver2
ps -ef | grep jupyter
```

Should only return the commands itself.
