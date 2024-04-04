```bash
start-all.sh
mr-jobhistory-daemon.sh start historyserver
# start-history-server.sh

nohup hive --service metastore > metastore.log &
nohup hive --service hiveserver2 > hiveserver.log &
nohup jupyter lab > error.log &
```
