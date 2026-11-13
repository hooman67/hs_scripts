```markdown
## Setup

```bash
conda activate sensei_toolkit
# set API key once in your laptop and once in the dev box
export ARTIFACTORY_UW2_API_TOKEN=AKCp8pRjGhLjY21du38okUBmbAWtKG7SkHYn3NrR5Cs2CC97x1Dmp1pQsfaHZHzQWkmt5F76A;
export ARTIFACTORY_UW2_USER=hshariati
```

**Connect to the VPN even if you’re in the office then run the following.**
```bash
sensei setup
```

Token from Artifactory: `cmVmdGtuOjAxOjE3MzA4Mjg4NTc6WEhpZWhpQU9pYjJpZ0pLeHpiQTRMTUd3RXNK`

[*] NOTE: Add the following line to your bash profile: `eval $(sed '/^\[/d' ~/.sensei/credentials | sed -E -n 's/[^#]+/export &/ p')`

## From Siavash

Add the following to your `.ssh/config` file:

```
HOST my_devbox_cont
    ProxyCommand ssh -W %h:%p hshariati@Session-d65c2cef-92b8-4c9b-a526-375a6ddfd838
    PasswordAuthentication yes
    HostName 127.0.0.1
    Port 4046 # this is your SSHD_PORT
    ServerAliveInterval 20
    ControlPersist 300
    User hshariati

Host my_devbox
    ProxyCommand ssh -W %h:%p %r@devbox6-2a-1-bastion.infra.adobesensei.io
    HostName Session-d65c2cef-92b8-4c9b-a526-375a6ddfd838.int.devbox.training.adobesensei.io
    PasswordAuthentication yes
    ControlMaster auto
    ServerAliveInterval 20
    ControlPersist 300
    User hshariati
```

Now you can do:

```bash
ssh my_devbox
```

to go to the devbox and you can do

```bash
ssh my_devbox_cont
```

To go directly to the Docker container.

## Connect to Devbox

First run this. **Make sure you're in VPN and type Y instead of just enter.**
```bash
sensei ssh -sid Session-d65c2cef-92b8-4c9b-a526-375a6ddfd838
```

After the above, then run this:
```bash
ssh hshariati@Session-d65c2cef-92b8-4c9b-a526-375a6ddfd838
```

Use your LDAP password.

For SSH debug use:
```bash
sensei devbox ssh_debug -sid <DEVBOX_ID>
```

## Start a Dev Box via CLI

```bash
sensei devbox start --arch cpu --min --disk_gb 100 --label hs_test_box_cli --tags asml_project_name:clio-next
```

## Use Docker in Dev Box

1.  SSH into the devbox:
    ```bash
    sensei ssh -sid Session-d65c2cef-92b8-4c9b-a526-375a6ddfd838
    ```
    Make sure you're connected to the VPN even in the office.
2.  Set Artifactory credentials:
    ```bash
    export ARTIFACTORY_UW2_API_TOKEN=AKCp8pRjGhLjY21du38okUBmbAWtKG7SkHYn3NrR5Cs2CC97x1Dmp1pQsfaHZHzQWkmt5F76A
    export ARTIFACTORY_UW2_USER=hshariati
    ```
3.  Set user permissions:
    ```bash
    chmod 755 /sensei-fs/users/hshariati/
    ```
4.  Set Docker permissions and login:
    ```bash
    sudo chmod 666 /var/run/docker.sock
    ```
    *** If you need a password for sudo use: `sensei`
    ```bash
    docker login -u $ARTIFACTORY_UW2_USER -p $ARTIFACTORY_UW2_API_TOKEN docker-matrix-experiments-snapshot.dr-uw2.adobeitc.com
    ```

## Add GitHub

1.  After running `sensei ssh` on your laptop, you’ll have a folder called:
    * `~/.ssh/.sensei/<DEVBOX_ID>.sensei.config`
    * In this file, find these lines (should be the first 3 lines in the file):
        * `HOST <DEVBOX_ID>`
        * `ProxyCommand ssh -W %h:%p %r@devbox6-2c-3-bastion.infra.adobesensei.io`
        * `Hostname <DEVBOX_ID>.int.devbox.training.adobesensei.io`
    * After these 3 lines add the following (make sure the indentation matches):
        ```
        IdentityFile ~/.ssh/id_ed25519
        User hshariati
        ControlMaster auto
        ControlPath /tmp/%C
        ServerAliveInterval 20
        RemoteForward 2000 git.corp.adobe.com:22
        RemoteForward 2001 artifactory.corp.adobe.com:443
        LocalForward 8265 127.0.0.1:8265
        LocalForward 9090 127.0.0.1:9090
        LocalForward 3000 127.0.0.1:3000
        ControlPersist 3000
        ControlMaster yes
        PasswordAuthentication yes
        User hshariati
        ```
2.  Now SSH into the devbox using `sensei ssh -sid <DEVBOX_ID>`.
3.  On the dev box, run these commands:
    ```bash
    mkdir ~/.ssh
    vim ~/.ssh/config
    ```
4.  Add these lines into the `~/.ssh/config` file:
    ```
    Host git.corp.adobe.com
      User git
      Port 2000
      Hostname 127.0.0.1
      Preferredauthentications publickey
      IdentityFile ~/.ssh/id_ed25519
    ```
5.  Copy your SSH key into the devbox:
    ```bash
    scp ~/.ssh/id_ed25519 Session-2a6d84e5-d045-4422-8414-628ed9465eea:~/.ssh/
    ```
6.  Now you can clone repos, push, etc. Note that the first time you might get a warning. Make sure you type `yes`.
7.  *** Remember you can only commit and push from your dev\_box, not from the containers. You can pull from containers though. The devbox uses port 2000 to communicate with GitHub and port 2001 to talk to Artifactory. For `my_colligo_cont`, you need to pull submodules from git. I had configured this on 2001 but then changed it to port 2004. I think this fixed the issue. I also added a line (similar to `my_colligo_cont` to the `my_devbox` for manual port forwarding). This was not mentioned in the docs, but it's what did the trick, I think.
8.  sdf

## Add VS Code

1.  If you added the lines From siavash. Then you just have to point the config path to `.ssh/config` and then you can just connect to the host or directly to the container from the remote explorer section of VS Code.
2.  Open the file: `~/.ssh/.sensei/Session-d65c2cef-92b8-4c9b-a526-375a6ddfd838.sensei.config`
3.  After these lines:
    ```
    HOST Session-d65c2cef-92b8-4c9b-a526-375a6ddfd838
        ProxyCommand ssh -W %h:%p %r@devbox6-2a-1-bastion.infra.adobesensei.io
        Hostname Session-d65c2cef-92b8-4c9b-a526-375a6ddfd838.int.devbox.training.adobesensei.io
    ```
4.  Add these lines (and make sure indentation matches):
    ```
        IdentityFile ~/.ssh/id_ed25519
        User hshariati
        ControlMaster auto
        ControlPath /tmp/%C
        ServerAliveInterval 20
        RemoteForward 2000 git.corp.adobe.com:22
        RemoteForward 2001 artifactory.corp.adobe.com:443
        LocalForward 8265 127.0.0.1:8265
        LocalForward 9090 127.0.0.1:9090
        LocalForward 3000 127.0.0.1:3000
        ControlPersist 3000
        ControlMaster yes
        PasswordAuthentication yes
        User hshariati
    ```
5.  In the "Remote - SSH" extensions setting, in the "The absolute file path to a custom SSH config file," add the path to this file: `~/.ssh/.sensei/Session-d65c2cef-92b8-4c9b-a526-375a6ddfd838.sensei.config`. You can also access this from: `Code > Preferences > Settings > Under User Settings click Extensions and choose Remote SSH: Config File`.
6.  Connect to host. If you get an error, this is because you're connected to another session. Kill/Restart VS Code and start another one.
7.  When it asks for a password, enter your LDAP.
8.  `Command + o` opens folders.
9.  `Command + p` is for searching files and everything else (type `>` to enter command mode).

## SSH Key Expiring

1.  Go to LDAP, click on services, then SSH Key, then Manage SSH Key.
2.  Generate a new SSH key (following the instructions LDAP gives you) and upload the public one.
3.  Connect to your devbox using `ssh hshariati@Session-d65c2cef-92b8-4c9b-a526-375a6ddfd838` and then replace the keys in the `.ssh` folder with the new one.
4.  Go to GitHub, delete the existing key and add the new one. Note that you will have to add two on GitHub: one for sign-in and one for authentication.
5.  You can also restart the SSH services if you see any error.
    a. For devbox use: `sudo service ssh restart`
    b. For Mac use:
        i. `sudo launchctl stop com.openssh.sshd`
        ii. `sudo launchctl start com.openssh.sshd`

## Restart the Whole Machine

```bash
sensei devbox switch -sid session-b02f7998-a598-47b7-8017-4a2fe272f64a --ports vscode:8888 dj:8889 tf:8890 st:8891 app1:8892 app2:8893 app3:8894
```

I'm using this: `Session-66e85cca-0365-423a-91df-78fdc00a812a`
```