# JupyterLab

## Installing a New Theme

1. Go to the `Extension Manager` (jigsaw icon) and `enable` the feature.
2. Search for `jupyterlab-theme-solarized-dark` and click `install`.
<!-- 3. We get an error, the node version is not up to date

   ```text
   Extension Installation Error
   An error occurred installing <code>jupyterlab-theme-solarized-dark</code>.

   Error message:

   Please install nodejs >=12.0.0 before continuing. nodejs may be installed using conda or directly from the nodejs website.
   ```

4. SSH into your machine and install a newer version of node

   ```bash
   curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
   sudo apt-get install -y nodejs
   ```

   verify that we have version 16.14.0:

   ```bash
   node --version
   #v16.19.1
   ``` -->

<!-- 5. Back in JupyterLab, try to install `jupyterlab-theme-solarized-dark` again.
6. In the upper left corner you should see: `A build is needed to include the latest changes`, click `Rebuild`.
7. If you want to see the current logs, create a new terminal `File > New > Terminal` and type `tail -f error.log`. -->
8. Refresh the Window.
9. Activate your new theme under `Settings > Theme > JupyterLab Solarized Dark`

## Installing Git Extension

1. Go to the `Extension Manager` (jigsaw icon).
2. Search for `git` and try(!) to install the `jupyterlab-git` extension.
3. Turns out, we need to restart the server:
7. Unfortunately, we don't have a `restart` options in the web-interface. However, we can at least stop the service with `File > Shut Down`.
8. As `hadoop` on your ssh session, check that the shutdown was successful with:

   ```bash
   # this command should only return one line, the grep itself. Otherwise `kill` the jupyterlab process.
   ps -ef | grep jupyter
   ```

9. Start the service again:

   ```bash
   nohup jupyter lab > error.log &
   ```

10. Back in the web-service, we should see the new `git` icon in the left menu bar and a `git` menu entry on top.
11. Let's `clone` the BLDC repository. Make sure that in the file browser you are in `/` (you should e.g. see the folder `hadoop` and the file `error.log`). Go to `Git > Clone a Repository` and paste the url `https://github.com/fred1234/BDLC_FS24` into the text field and hit `Clone`.
