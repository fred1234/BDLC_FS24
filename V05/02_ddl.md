# Data Definition Language - DDL

Hive provides a DDL for creating and managing databases, tables and for inserting data.

Open a `hive` CLI session with:

```bash
beeline -n hadoop -u jdbc:hive2://localhost:10000
```

```sql
SHOW DATABASES;
```

```sql
CREATE DATABASE IF NOT EXISTS test_db;
```

you should see the `test_db` folder in http://bdlc-XX.el.eee.intern:9870/explorer.html#/user/hive/warehouse/

```sql
USE test_db;
CREATE TABLE IF NOT EXISTS test_table (id bigint not null, value varchar(100));
SHOW TABLES;
```

Let us insert some data:

```sql
INSERT INTO test_table (id, value) VALUES (1,'ABC'), (2,'DEF');
```

This triggers a MapReduce job. Check it out in YARN http://bdlc-XX.el.eee.intern:8088/cluster

```sql
SELECT * FROM test_table;
```

## HIVE SQL in `JupyterLab`

It is more comfortable to work in `JupyterLab`. You can test the Notebook in `BDLC_FS23/V05/resources/Testing_Hive.ipynb`.

## References

- [Hive Tutorials](https://data-flair.training/blogs/apache-hive-tutorial/)
- [Official Website Tutorials](https://cwiki.apache.org/confluence/display/Hive/GettingStarted#GettingStarted-MovieLensUserRatings)
