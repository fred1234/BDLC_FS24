# Taxi

- [official site](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
- As user `student`, create the folder `/data/dataset_cluster/` and give the `cluster` user permission:

```bash
sudo mkdir /data/dataset_cluster/
sudo chown cluster:root -R /data/dataset_cluster/
```

- The rest can be executed as user `cluster`.

## Create Raw HDFS directory

```bash
hdfs dfs -mkdir -p /taxi/raw
```

## Downloader

Create a folder `/data/dataset_cluster/taxi` and add the bash script to a file called `downloader.sh`

```bash
#!/usr/bin/env bash

#https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page

for year in {2009..2021}; do
    echo Year - $year
    mkdir ./$year
    hdfs dfs -mkdir /taxi/raw/$year
    for month in {01..12}; do
        echo -e "\t Month - $month"

        year_date=$year-$month
        url=https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_${year_date}.parquet

        wget $url -O ./$year/yellow_tripdata_${year_date}.parquet

        hdfs dfs -Ddfs.replication=1 -put ./$year/yellow_tripdata_${year_date}.parquet /taxi/raw/$year
    done
done

```

```bash
chmod 755 downloader.sh
```

```bash
./downloader.sh
```
