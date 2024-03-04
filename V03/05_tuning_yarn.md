# Tuning our Cluster

In the example of the word count with the 10 gigs we saw two major drawbacks.

1. We spill our intermediate results to `/` and not to `/data`.
2. Not all CPUs are used and more memory could be used.

## Change Spilling Directory

Create the new tmp directory as `student`:

```bash
sudo mkdir /data/tmp/
sudo chown hadoop:root -R /data/tmp/
```

Change to user `hadoop` and stop all Hadoop services:

```bash
stop-all.sh
mr-jobhistory-daemon.sh stop historyserver
```

Change the `hadoop.tmp.dir` attribute by adding the following `<property>` attribute to `~/hadoop/etc/hadoop/core-site.xml`:

```xml
<property>
  <name>hadoop.tmp.dir</name>
  <value>/data/tmp/hadoop-${user.name}</value>
</property>
```

Let's wait to start the service as we have more configs to change.

### Additional Information About Spilling

As written [here](https://stackoverflow.com/questions/27890887/why-does-hadoop-spilling-happens/27907019) and [here](https://data-flair.training/forums/topic/explain-the-process-of-spilling-in-mapreduce/]):

> Spilling happens when there is not enough memory to fit all the mapper output. Amount of memory available for this is set by `mapreduce.task.io.sort.mb`
>
> It happens when 80% of the buffer space occupied because the spilling is done in a separate thread, not to interfere with mapper. If the buffer reaches 100% utilization, the mapper thread has to stop and wait for the spilling thread to free up the space. To avoid this, the threshold of 80% is chosen
>
> Spilling happens at least once, when the mapper finished, because the output of the mapper should be sorted and saved to the disk for reducer processes to read it. And there is no use to invent a separate function to the last "save to disk", because in general it does the same task

## Increasing CPU and Memory

Also as `hadoop` add the following two `<poperty>`-tags to `~/hadoop/etc/hadoop/yarn-site.xml`:

```xml
  <property>
    <name>yarn.nodemanager.resource.detect-hardware-capabilities</name>
    <value>true</value>
  </property>
```

### Additional Information About Resource Management

- [blog post](https://blog.damavis.com/en/first-steps-with-apache-yarn-customization/)
- [yarn defaults](https://hadoop.apache.org/docs/r3.3.6/hadoop-yarn/hadoop-yarn-common/yarn-default.xml)

## Start the Hadoop Services

```bash
start-all.sh
mr-jobhistory-daemon.sh start historyserver
```

Go to the [Resource Manager](http://bdlc-XX.labservices.ch:8088/) and see the new resources we have for the cluster. :heart:

```text
Total Resources
<memory:18.81 GB, vCores:20>
```
