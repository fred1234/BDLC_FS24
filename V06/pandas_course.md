# Pandas

This week we will do this external [Pandas Workshop](https://github.com/stefmolin/pandas-workshop/tree/main) which was first delivered at [ODSC Europe 2021](https://odsc.com/speakers/introduction-to-data-analysis-using-pandas/).

The workshop is created by Stefanie Molin, data scientist and software engineer at Bloomberg in New York City:

> Working with data can be challenging: it often doesn’t come in the best format for analysis, and understanding it well enough to extract insights requires both time and the skills to filter, aggregate, reshape, and visualize it. This session will equip you with the knowledge you need to effectively use pandas – a powerful library for data analysis in Python – to make this process easier.

The Course has four sections:

- Section 1: Getting Started With Pandas
- Section 2: Data Wrangling
- Section 3: Data Visualization
- Section 4: Hands-On Data Analysis Lab

## Course Outline

The notebooks (where you work) are saved under the folder `notebooks`. The solutions are under `slides`.

Make sure that you have `[ OK ]` in all environment checks in the first notebook called `0-check_your_env.ipynb` by **running** the cell:
![image](https://user-images.githubusercontent.com/646839/159240004-d2c3efb2-40fa-489a-9b95-96063df4f689.png)

## Running the Pandas Workshop Course

You have two options: online or on your cluster.

### Running the Course Online

By using this [link](https://mybinder.org/v2/gh/stefmolin/pandas-workshop/main?urlpath=lab) one can participate without the need to install something. Drawback, however, is that saving the notebooks is more cumbersome as you have to download the notebooks on your own. In other words, re-visiting the link opens a new and blank course again.

## Running the Course on your Cluster

All the files are saved automatically for you. However, there are a few steps (always the same 😉) to setup the course.

### Setup the Course on your Cluster

1. SSH into your machine with `ssh student@bdlc-XX.labservices.ch`, where `XX` is your personal virtual machine number.
<!-- 2. Install the virtual environment package for python: `sudo apt install -y python3-venv` -->
2. Switch to user hadoop: `su - hadoop`
3. Stop "your" JupyterLab instance:

   ```bash
   ps -ef | grep jupyter-lab
   ```

   e.g output like:

   ```text
   hadoop    152556  152476  6 11:06 pts/0    00:00:01 /usr/bin/python3 /home/hadoop/.local/bin/jupyter-lab
   ```

   Then kill the process with:

   ```bash
   kill 152556
   ```

4. http://bdlc-XX.labservices.ch:8888/lab?, where `XX` is your personal virtual machine number, should no longer be reachable.
5. In the ssh session, create a new folder for the workshop. `mkdir ~/pandas-workshop`.
6. Change directory to the folder `cd ~/pandas-workshop`
7. Clone the pandas workshop from git: `git clone https://github.com/stefmolin/pandas-workshop.git`
8. Create a virtual enviornment (venv) for the workshop with `python3 -m venv pandas_workshop_venv`.
9. Activate the venv `source pandas_workshop_venv/bin/activate`.
   1. The prompt of your shell should change from e.g.: `(venv) hadoop@bdlc-20:~/pandas-workshop$` to: `(pandas_workshop_venv) hadoop@bdlc-20:~/pandas-workshop$`
10. Change to the workshop-folder:

    ```bash
    cd pandas-workshop/
    ```

    e.g.

    ```bash
    (pandas_workshop_venv) hadoop@bdlc-19:~/pandas-workshop$ cd pandas-workshop/
    (pandas_workshop_venv) hadoop@bdlc-20:~/pandas-workshop/pandas-workshop$ pwd
    /home/hadoop/pandas-workshop/pandas-workshop
    ```

11. Install the necessary python libraries with `pip3 install -r requirements.txt`.
12. Start the workshop with `jupyter lab`.
13. As long as the shell is open, you can access [http://bdlc-XX.labservices.ch:8888/lab](http://bdlc-XX.labservices.ch:8888/lab).
    1. Use your `jupyterlab` password.
    2. You can dismiss the warnings: `jupyterlab-git server extension`.

Note, if you logout from your session, the `jupyter daemon` is no longer listening. If you want to continue with the course, just activate the venv again and start `jupyterlab`, e.g.

```bash
source ~/pandas-workshop/pandas_workshop_venv/bin/activate
cd ~/pandas-workshop/pandas-workshop/
jupyter lab
```
