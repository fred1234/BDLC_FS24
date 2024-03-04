# Preparing Dataset

> As user `student`.

Right now, our `/data/` folder looks like this:

```bash
student@bdlc-20:~$ ls -lisa /data/
total 28
      2  4 drwxr-xr-x  4 root   root  4096 Mar  1 15:12 .
      2  4 drwxr-xr-x 21 root   root  4096 Mar  1 13:47 ..
9043969  4 drwxr-xr-x  4 hadoop root  4096 Mar  1 15:12 hdfs
     11 16 drwx------  2 root   root 16384 Mar  1 13:47 lost+found
student@bdlc-20:~$
```

Let us create a folder where we store the data when we want to test algorithms outside of `hdfs`.

```bash
sudo mkdir -p /data/dataset/text
```

As we want to operate with user `hadoop`, let's give the right permissions:

```bash
sudo chown hadoop:root -R /data/dataset/
```

Now we can switch back to user `hadoop`.

```bash
su - hadoop
```

Change directory to `/data/dataset/text/`.

```bash
cd /data/dataset/text/
```

## Small Text File

A very small text file helps us to check our algorithms:

```bash
echo 'Der aus dem englischen Sprachraum stammende Begriff Big Data steht in engem Zusammenhang mit dem umfassenden Prozess der Datafizierung und bezeichnet Datenmengen, welche beispielsweise zu gross, zu komplex, zu schnelllebig oder zu schwach strukturiert sind, um sie mit manuellen und herkömmlichen Methoden der Datenverarbeitung auszuwerten.' >> small.txt
```

## Holmes

*The adventures of sherlock holmes* should still be in your home directory `~`

```bash
mv ~/holmes.txt .
```

If not, just download the text again from project gutenberg:

```bash
wget https://www.gutenberg.org/files/1661/1661-0.txt -O ~/holmes.txt
```

## Big Text File

Download the file with:

```bash
wget https://drive.switch.ch/index.php/s/ev7rTiofreTtiC5/download -O gutenberg.tar.bz2
```

extract the folder (this takes a while ~ 20 minutes):

```bash
tar -xvf gutenberg.tar.bz2
```

and finally remove the `bz2` file:

```bash
rm gutenberg.tar.bz2
```

### More Information on the dataset

- If you are interested how I downloaded the corpus, check this [repository](https://github.com/pgcorpus/gutenberg)
- And more information about project gutenberg are [here](https://www.gutenberg.org)

## Copy the files to `hdfs`

Remove the `/dataset` folder on `hdfs` with:

```bash
hdfs dfsadmin -safemode leave
```

```bash
hdfs dfs -rm -r /dataset
```

and copy the needed dataset folder to `hdfs`:

```bash
hdfs dfs -mkdir -p /dataset/text
hdfs dfs -put /data/dataset/text/*.txt /dataset/text/
hdfs dfs -put /data/dataset/text/gutenberg/gutenberg_singleFile/gutenberg_all.txt /dataset/text/
```

## Checking Available Space on `/data/`

It is always a good idea to keep the the disk size under control.
Let's check how much space we use on `/data`.

```bash
df -h | grep '/data'
```

returns something like:

```text
/dev/sdb                           147G   31G  109G  22% /data
```

In other words, 22% of the space is used. So far, so good.

## Symbolic Link from Home Directory to `/data/dataset`

When we operate in `jupyter lab`, we see all folders relative to `/home/hadoop/`. Let's create a symbolic link so we can switch easily to `/data/dataset`:

```bash
ln -s /data/dataset/ ~/dataset
```
