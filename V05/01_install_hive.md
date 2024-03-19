# Hive

## Stopping all Hadoop Services

Change to user `hadoop` (`su - hadoop`) and stop all Hadoop services:

```bash
stop-all.sh
mr-jobhistory-daemon.sh stop historyserver
```

## Installing and Configuring Java 8, MySQL and MySQL Connector

As user `student`

### Java 1.8

Install Java:

```bash
#sudo apt install openjdk-8-jdk openjdk-8-jre
sudo apt install -y openjdk-8-jdk
```

As we have three Java versions now, we have to pick the default one. Execute:

```bash
sudo update-alternatives --config java
```

and choose the `/usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java` by providing the right number:

```text
There are 2 choices for the alternative java (providing /usr/bin/java).

  Selection    Path                                            Priority   Status
------------------------------------------------------------
* 0            /usr/lib/jvm/java-11-openjdk-amd64/bin/java      1111      auto mode
  1            /usr/lib/jvm/java-11-openjdk-amd64/bin/java      1111      manual mode
  2            /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java   1081      manual mode

Press <enter> to keep the current choice[*], or type selection number: 2
```

The Java version should now be `1.8.0_312`:

```bash
java -version
```

```text
openjdk version "1.8.0_312"
OpenJDK Runtime Environment (build 1.8.0_312-8u312-b07-0ubuntu1~20.04-b07)
OpenJDK 64-Bit Server VM (build 25.312-b07, mixed mode)
```

## MySQL Connector

We need a library so that Java can communicate with MySQL:

```bash
wget https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java_8.0.28-1ubuntu20.04_all.deb
```

```bash
sudo apt install -y ./mysql-connector-java_8.0.28-1ubuntu20.04_all.deb
```

## JAVA HOME for Hadoop

As user `hadoop`, we have to change the `JAVA_HOME` location so we are using Java 1.8.

```bash
su - hadoop
```

Edit the file `~/hadoop/etc/hadoop/hadoop-env.sh` (this can also be done in `JupyterLab`) and change the line:

from `export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64` to:

```bash
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64
```

And in `~/hadoop/etc/hadoop/core-site.xml`, add the properties:

```xml
    <property>
      <name>hadoop.proxyuser.hadoop.hosts</name>
      <value>*</value>
   </property>
   <property>
      <name>hadoop.proxyuser.hadoop.groups</name>
      <value>*</value>
   </property>
```

Let us start the hadoop services again:

```bash
start-all.sh
mr-jobhistory-daemon.sh start historyserver
```

Verify that `hdfs` is running by doing a:

```bash
hdfs dfs -ls /
```

## Installing HIVE

Still as user `hadoop`, download, extract and rename `hive`:

```bash
wget https://dlcdn.apache.org/hive/hive-3.1.3/apache-hive-3.1.3-bin.tar.gz
tar -xvzf apache-hive-3.1.3-bin.tar.gz
mv apache-hive-3.1.3-bin hive
```

Let's add the following block to the **end** of `~/.bashrc`:

```text
# Hive
export JAVA_HOME='/usr/lib/jvm/java-1.8.0-openjdk-amd64'
export HIVE_HOME='/home/hadoop/hive/'
export PATH=$PATH:$HIVE_HOME/bin
```

```bash
nano ~/.bashrc
```

Source `~/.bashrc` to load the configuration we just made:

```bash
source ~/.bashrc
```

### Initialize HDFS for Hive

Let us create a `hive` user folder in `hdfs`:

```bash
hdfs dfs -mkdir /user/hive/
```

Run the following helper script which setups the right permissions and creates `/user/hive/warehouse`:

```bash
init-hive-dfs.sh
```

```text
init-hive-dfs.sh
Setting writeable group rights for directory [/tmp]
Setting writeable group rights for directory [/user/hive/warehouse]
Initialization done.

Please, do not forget to set the following configuration properties in hive-site.xml:
hive.metastore.warehouse.dir=/user/hive/warehouse
hive.exec.scratchdir=/tmp
```

### GUAVA Problems

Unfortunately we have to deal with a library conflict. Execute:

```bash
ls $HADOOP_HOME/share/hadoop/common/lib | grep guava
ls $HIVE_HOME/lib | grep guava
rm $HIVE_HOME/lib/guava-19.0.jar
cp $HADOOP_HOME/share/hadoop/common/lib/guava-27.0-jre.jar $HIVE_HOME/lib/
```

### Create User Hive in MySQL

We will create an own hive user in the `MySQL` database. Still as user `hadoop`:

```bash
mysql -u root
```

```sql
CREATE USER 'hive'@'localhost' IDENTIFIED BY 'hive' password expire never;
GRANT ALL ON *.* TO 'hive'@'localhost';
exit;
```

We can set the password of hive with the first login:

```bash
mysql -u hive -phive
```

Let's create a new database for the `hive_metastore`:

```sql
create database hive_metastore;
show databases;
exit;
```

Our credentials and meta_store informations are therefore:

- user: `hive`
- password: `hive`
- database: `hive_metastore`

## MYSQL Connector

We now point to the java mysql connector so hive knows how to speak with the database.

```bash
ln -s /usr/share/java/mysql-connector-java-8.0.28.jar /home/hadoop/hive/lib/mysql-connector-java.jar
```

### HIVE Config

We also have to make changes in `hive-site.xml`

Basically, we need to adjust these properties:

- `javax.jdo.option.ConnectionDriverName`: `com.mysql.cj.jdbc.Driver`
- `javax.jdo.option.ConnectionURL`: `jdbc:mysql://localhost/hive_metastore`
- `javax.jdo.option.ConnectionUserName`: `hive`
- `javax.jdo.option.ConnectionPassword`: `hive`
- `hive.metastore.uris`: `thrift://127.0.0.1:9083`
- `hive.metastore.db.type`: `mysql`

I have already prepared this changes. So let us download the `hive-site.xml` with:

```bash
wget https://raw.githubusercontent.com/fred1234/BDLC_FS24/main/V05/resources/hive-site.xml -O ~/hive/conf/hive-site.xml
```

<!-- ```bash
cd ~/hive/conf/
cp hive-default.xml.template hive-site.xml
cp hive-env.sh.template hive-env.sh
```

Change the values accordingly:

```xml
<property>
   <name>javax.jdo.option.ConnectionDriverName</name>
   <value>com.mysql.cj.jdbc.Driver</value>
</property>
<property>
   <name>javax.jdo.option.ConnectionURL</name>
   <value>jdbc:mysql://localhost/hive_metastore</value>
</property>
<property>
    <name>javax.jdo.option.ConnectionUserName</name>
    <value>hive</value>
  </property>
<property>
   <name>javax.jdo.option.ConnectionPassword</name>
   <value>hive</value>
</property>
<property>
   <name>hive.metastore.uris</name>
   <value>thrift://127.0.0.1:9083</value>
</property>
<property>
   <name>hive.metastore.db.type</name>
   <value>mysql</value>
</property>
``` -->

<!-- ## Configure Hive API authentication

In `~/hive/conf/hive-site.xml`, change the property:

```xml
<property>
    <name>hive.metastore.event.db.notification.api.auth</name>
     <value>false</value>
     <description>
       Should metastore do authorization against database notification related APIs such as get_next_notification.
       If set to true, then only the superusers in proxy settings have the permission
     </description>
   </property>
``` -->

<!-- I've got:

```bash
java.lang.RuntimeException: Error applying authorization policy on hive configuration: java.net.URISyntaxException: Relative path in absolute URI: ${system:java.io.tmpdir%7D/$%7Bsystem:user.name%7D
```

Solution (in this [SO](https://stackoverflow.com/questions/27099898/java-net-urisyntaxexception-when-starting-hive/42945230#42945230)) was that in `~/hive/conf/hive-site.xml`, change the property:

```xml
<property>
     <name>hive.exec.local.scratchdir</name>
 <value>/tmp/${user.name}</value>
  </property>
  <property>
<name>hive.downloaded.resources.dir</name>
<value>/tmp/${user.name}_resources</value>
  </property>
``` -->

## Initialize Database Structure

There is also a helper script to initialize the `metastore` database.

```bash
schematool -dbType mysql -initSchema
```

You should see:

```text
Initialization script completed
schemaTool completed
```

Verify the meta store tables have been created.

### Checking the Created Metastore - With the CLI

```bash
mysql -u hive -p
```

```sql
use hive_metastore;
show tables;
exit;
```

### Checking the Created Metastore - With `JupyterLab`

We can run SQL directly in `JupyterLab`. Open a terminal in `Jupyterlab` and install:

```bash
pip install pyhive
pip install pyhive[hive]
```

<!-- TODO - link to FORUM

Afterwards you can test the Notebook in `BDLC_FS23/V04/resources/Testing_MYSQL.ipynb`. If you don't see it, you need to pull the newest files from `github` first `Git > Pull from Remote`.
(Please also checkout the forum entry about making a [backup](https://elearning.hslu.ch/ilias/ilias.php?ref_id=5324442&cmdClass=ilobjforumgui&thr_pk=55627&page=0&cmd=viewThread&cmdNode=10f:qo&baseClass=ilrepositorygui)). -->

## Starting Hive

Starting the `metastore`:

```bash
#hive --service metastore
nohup hive --service metastore > metastore.log &
```

```bash
#hive --service hiveserver2
nohup hive --service hiveserver2 > hiveserver.log &
```

Check out the logs in `/tmp/hadoop/hive.log`. We should not see any errors, except the `java.lang.NoClassDefFoundError: org/apache/tez/dag/api/TezConfiguration` Exception.

:sparkles: - You have installed Hive - :sparkles:

Check out http://bdlc-XX.el.eee.intern:10002/

To start a CLI session with `hive` type:

```bash
beeline -n hadoop -u jdbc:hive2://localhost:10000
```

To see the databases, type:

```text
jdbc:hive2://localhost:10000> show DATABASES;
+----------------+
| database_name  |
+----------------+
| default        |
+----------------+
```

<!-- ### SQL Extensions

As `hadoop`, stop `JupyterLab`:

```bash
ps -ef | grep jupyter
# followed by the kill pid command
```

Install the following extension and build it:

```bash
pip install jupyterlab_sql
jupyter serverextension enable jupyterlab_sql
jupyter lab build
```

Start `JupyterLab` again with

```bash
nohup jupyter lab > error.log &
``` -->

## Creating a Database / a Table and Inserting Data

Let us go to the [Data Definition Language](./02_ddl.md) document.

## References

- [Hive's website](https://cwiki.apache.org/confluence/display/Hive/Home)
- [Installing Hive on Linux](https://kontext.tech/column/hadoop/561/apache-hive-312-installation-on-linux-guide)
