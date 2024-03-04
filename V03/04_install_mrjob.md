# MrJob

## Why MRJob

MrJob is a tool which makes it easier to write MapReduce algorithms.

What makes the streaming API unpleasant?

- One has to write the mapper and the reducer into separate files.
- Often, one MapReduce is the input to another MapReduce algorithm which makes the above point even more cumbersome.
- Testing the algorithm locally needs adjustments (e.g. `sort`-trick with Unix)

From the official [website](https://mrjob.readthedocs.io/en/latest/):
>mrjob lets you write MapReduce jobs in Python 2.7/3.4+ and run them on several platforms. You can:
>
>- Write multi-step MapReduce jobs in pure Python
>- Test on your local machine
>- Run on a Hadoop cluster
>- Run in the cloud using Amazon Elastic MapReduce (EMR)
>- Run in the cloud using Google Cloud Dataproc (Dataproc)
>- Easily run Spark jobs on EMR or your own Hadoop cluster
>
>Here are a number of features of mrjob that make writing MapReduce jobs easier:
>
>- Keep all MapReduce code for one job in a single class
>- Easily upload and install code and data dependencies at runtime
>- Switch input and output formats with a single line of code
>- Automatically download and parse error logs for Python tracebacks
>- Put command line filters before or after your Python code

## Installation

As user `hadoop` (you can also use the built in terminal from `jupyterlab`) use:

```bash
pip install mrjob
```

## References

- [mrjob website](https://mrjob.readthedocs.io/en/latest/)
