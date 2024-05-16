# Master Setup

| Machine                | Short Description |
| ---------------------- | ----------------- |
| bdlc-15.labservices.ch | Master            |
| bdlc-16.labservices.ch | Slave 1           |
| bdlc-17.labservices.ch | Slave 2           |

Follow these steps as user `cluster` on your `master` node.

## Keys

Create a Key

```bash
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 0600 ~/.ssh/authorized_keys
```

Copy the key to all machines:

```bash
ssh-copy-id cluster@bdlc-15.labservices.ch
ssh-copy-id cluster@bdlc-16.labservices.ch
ssh-copy-id cluster@bdlc-17.labservices.ch
```

You can now `ssh` from master into all machines. Verify this with:

```bash
ssh bdlc-15.labservices.ch
ssh bdlc-16.labservices.ch
ssh bdlc-17.labservices.ch
```

## bashrc

Edit your bash profile in `~/.bashrc` and add these lines at the end:

```text
# Hadoop
export PDSH_RCMD_TYPE=ssh
export HADOOP_HOME=/home/cluster/hadoop
export PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin

# Spark
export SPARK_HOME=/home/cluster/spark
export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
```

```bash
nano ~/.bashrc
```

Activate the changes with:

```bash
source ~/.bashrc
```

Copy the ~./bashrc to all other nodes.

```bash
scp /home/cluster/.bashrc bdlc-16.labservices.ch:/home/cluster/.bashrc
scp /home/cluster/.bashrc bdlc-17.labservices.ch:/home/cluster/.bashrc
```

## Setup Github Repo (optional)

Create a [new Github Repo](https://docs.github.com/en/get-started/quickstart/create-a-repo)

### Adding a Deploy Key

Following this [guide](https://docs.github.com/en/developers/overview/managing-deploy-keys), add your public key to github:

```bash
cat ~/.ssh/id_rsa.pub
```

Make sure to check the `Allow write access` option.

### Cloning your Repository

```bash
cd ~
git clone git@github.com:fred1234/BDLC_FS24_Project_Template.git
cd BDLC_FS24_Project_Template/
```

```bash
git config  user.email "Cluster User"
git config  user.name "Cluster User"
```

Try to create a new file and see if `commit`/`push` works.

```bash
cluster@bdlc-19:~/BDLC_FS24_Project_Template$ echo "19" >  19_file
cluster@bdlc-19:~/BDLC_FS24_Project_Template$ git add 19_file
cluster@bdlc-19:~/BDLC_FS24_Project_Template$ git commit -m "adding a 19file"
[main dc4d0f8] adding a 19file
 1 file changed, 1 insertion(+)
 create mode 100644 19_file

cluster@bdlc-19:~/BDLC_FS24_Project_Template$ git push
Enumerating objects: 4, done.
Counting objects: 100% (4/4), done.
Delta compression using up to 20 threads
Compressing objects: 100% (2/2), done.
Writing objects: 100% (3/3), 269 bytes | 269.00 KiB/s, done.
Total 3 (delta 1), reused 0 (delta 0)
remote: Resolving deltas: 100% (1/1), completed with 1 local object.
To github.com:fred1234/BDLC_FS24_Project_Template.git
   24d86e2..dc4d0f8  main -> main
cluster@bdlc-19:~/BDLC_FS24_Project_Template$
```

## HDFS and Hadoop

We need to configure:

- The Java version
- The entry point for HDFS namenode
- The replication factor
- The name and replication dir
- The block size (if [necessary](https://stackoverflow.com/questions/2669800/change-block-size-of-dfs-file#:~:text=value%20of%20dfs.-,block.,2.0%20default%20size%20is%20128MB.))
- The secondary namenode
- Where the datanodes are

### JAVA Version

We need to specify `JAVA_HOME` in `~/hadoop/etc/hadoop/hadoop-env.sh`.

```text
change the line from
# export JAVA_HOME=
```

to

```text
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64
```

with

```bash
nano ~/hadoop/etc/hadoop/hadoop-env.sh
```

### `core-site.xml`

Replace / add the configuration part in `~/hadoop/etc/hadoop/core-site.xml` with the content:

```xml
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://bdlc-15.labservices.ch:9000</value>
    </property>
</configuration>
```

```bash
nano ~/hadoop/etc/hadoop/core-site.xml
```

Use your master instead of `bdlc-15.labservices.ch`.

### `hdfs-site.xml`

for `~/hadoop/etc/hadoop/hdfs-site.xml` with:

```xml
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>2</value>
    </property>
    <property>
        <name>dfs.secondary.http.address</name>
        <value>bdlc-16.labservices.ch:50090</value>
    </property>
    <property>
        <name>dfs.name.dir</name>
        <value>file:///data/hdfscluster/namenode</value>
    </property>
    <property>
        <name>dfs.data.dir</name>
        <value>file:///data/hdfscluster/datanode</value>
    </property>
    <property>
        <name>dfs.namenode.datanode.registration.ip-hostname-check</name>
	    <value>false</value>
    </property>
</configuration>
```

```bash
nano ~/hadoop/etc/hadoop/hdfs-site.xml
```

### Workers

Add all datanodes to this file:

```bash
nano  ~/hadoop/etc/hadoop/workers
```

E.g.

```text
bdlc-15.labservices.ch
bdlc-16.labservices.ch
bdlc-17.labservices.ch
```

### Copy the Changes to the Slaves

Copy all the config changes to the slaves:

```bash
scp /home/cluster/hadoop/etc/hadoop/* bdlc-16.labservices.ch:/home/cluster/hadoop/etc/hadoop/
scp /home/cluster/hadoop/etc/hadoop/* bdlc-17.labservices.ch:/home/cluster/hadoop/etc/hadoop/
```

### Formatting HDFS

Format the namenode.

```bash
hdfs namenode -format
```

### Starting HDFS and Checks

```bash
start-dfs.sh
```

Go to http://bdlc-15.labservices.ch:9870/ and verify that we have all nodes in the cluster.

Check that the command

```bash
hdfs dfs -ls /
```

Does not return a failure.

## Spark

We need to configure:

- Where the Hadoop configs are
- Where workers are
- What the master address is
- Where to save logs in HDFS (and create this folder in HDFS)

### `spark-defaults.conf`

Let's create the HDFS folder for the `Spark History Server`.

```bash
hdfs dfs -mkdir -p /user/spark/spark-logs
```

```bash
cp ~/spark/conf/spark-defaults.conf.template ~/spark/conf/spark-defaults.conf
```

Let's add the following block to the **end** of `spark-defaults.conf`:

```text
spark.master spark://bdlc-15.labservices.ch:7077

spark.eventLog.enabled true
spark.eventLog.dir hdfs://bdlc-15.labservices.ch:9000/user/spark/spark-logs
spark.history.provider org.apache.spark.deploy.history.FsHistoryProvider
spark.history.fs.logDirectory hdfs://bdlc-15.labservices.ch:9000/user/spark/spark-logs
spark.history.fs.update.interval 10s
spark.history.ui.port 18080

spark.submit.deployMode client

spark.driver.memory 10g

spark.executor.memory 15g
spark.executor.instances 11
spark.executor.cores 4
```

```bash
nano ~/spark/conf/spark-defaults.conf
```

### `spark-env.sh`

```bash
cp ~/spark/conf/spark-env.sh.template ~/spark/conf/spark-env.sh
```

and add the following content to the **end** of `spark-env.sh`:

```bash
HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
SPARK_LOCAL_DIRS=/data/tmpcluster
SPARK_MASTER_HOST=bdlc-15.labservices.ch
```

```bash
nano ~/spark/conf/spark-env.sh
```

### `workers`

```bash
cp ~/spark/conf/workers.template ~/spark/conf/workers
```

and add the following content to the `workers` file:

```text
bdlc-15.labservices.ch
bdlc-16.labservices.ch
bdlc-17.labservices.ch
```

```bash
nano ~/spark/conf/workers
```

### Copy the Changes to the other Machines

Copy all the config changes to the slaves:

```bash
scp /home/cluster/spark/conf/* bdlc-16.labservices.ch:/home/cluster/spark/conf/
scp /home/cluster/spark/conf/* bdlc-17.labservices.ch:/home/cluster/spark/conf/
```

### Less Memory and CPU for Worker on Master

As the driver and other services (like Jupyter) will run on the master node as well, we shrink the resources on the master a bit.

#### `spark-env.sh` on Master

`spark-env.sh` with the two additional options: `SPARK_WORKER_CORES` and `SPARK_WORKER_MEMORY`.

```bash
HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
SPARK_LOCAL_DIRS=/data/tmpcluster
SPARK_MASTER_HOST=bdlc-15.labservices.ch
SPARK_WORKER_CORES=12
SPARK_WORKER_MEMORY=45g
```

```bash
nano ~/spark/conf/spark-env.sh
```

### Starting Spark Standalone Mode

```bash
~/spark/sbin/start-all.sh
```

### Starting the History Server

```bash
start-history-server.sh
```

### Checks

Go to http://bdlc-15.labservices.ch:8080/ and verify that we have the assigned resources.

Check that the command

```bash
spark-submit --deploy-mode client --class org.apache.spark.examples.SparkPi /home/cluster/spark/examples/jars/spark-examples_2.12-3.5.1.jar 10
```

Does not return a failure.

Check also that the history server is running on http://bdlc-15.labservices.ch:18080/.

### Python venv and Packages

```
python3 -m venv venv
```

Edit your bash profile in `~/.bashrc` and add these three lines at the end:

```text
#activate our python venv
source ~/venv/bin/activate
```

```bash
nano ~/.bashrc
```

Activate the changes with:

```bash
source ~/.bashrc
```

```bash
pip install markupsafe==2.0.1
pip install jupyterlab
pip install jupyterlab-git
pip install SQLAlchemy==1.3.24
pip install pandas
pip install ipython-sql
pip install pyarrow
pip install findspark
pip install sparksql-magic
pip install wordcloud
```

<!-- ```bash
wget https://raw.githubusercontent.com/fred1234/BDLC_FS24/main/V10/freeze.txt
pip install freeze.txt
``` -->

### JupyterLab

```bash
jupyter-lab --generate-config
```

If this command does not work, sign out of your session (type `exit` until you are back on your local machine). Sign in again and the above command should work.

```bash
jupyter-lab password
```

Copy the hashed password starting from `argon` to the end.

```bash
cat /home/cluster/.jupyter/jupyter_server_config.json
```

## Configs

```bash
nano /home/cluster/.jupyter/jupyter_lab_config.py
```

Change the password settings from `# c.ServerApp.password = ''` to your personal password:

```text
c.ServerApp.password = 'argon2:$argon2id$v=19$m=10240,t=10,p=...YOUR_HASH...'
```

`JupyterLab` can't be accessed remotely by default. Let's change that by
setting the listen ip from `# c.ServerApp.ip = 'localhost'` to:

```python
c.ServerApp.ip = '*'
```

and the default port `# c.ServerApp.port = 0` to:

```python
c.ServerApp.port = 8888
```

Start the service with:

```bash
jupyter lab
```

And test the service in your web-browser with the url `http://bdlc-XX.labservices.ch:8888/lab`

close the running service (`ctrl-c twice`) and start jupyter as a service

```bash
nohup jupyter lab > jupyter.log &
```

The service should still be accessible via `http://bdlc-XX.labservices.ch:8888/lab`.

# Services Overview

| Service              | Port  | Example                                |
| -------------------- | ----- | -------------------------------------- |
| HDFS Hadoop Overview | 9870  | http://bdlc-15.labservices.ch:9870/    |
| JupyterLab           | 8888  | http://bdlc-15.labservices.ch:8888/lab |
| Spark Cluster Master | 8080  | http://bdlc-15.labservices.ch:8080/    |
| Spark History Server | 18080 | http://bdlc-15.labservices.ch:18080/   |
