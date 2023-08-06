# sshcon ⚡

> Python SSH connector for linux systems

Python SSH connector for linux systems based on super fast SSH2 protocol library -> [ssh2-python](https://github.com/ParallelSSH/ssh2-python).

## Installation

```shell
pip install sshcon
```

## How to use

Make sure you check **[readthedocs](https://sshcon.readthedocs.io/en/latest/)**!

```python
from sshcon.main import SshCon


hostname = "myserver"
ssh_user = "myuser"
ssh_key = "/home/user/.ssh/mykey"
ssh = SshConn(hostname, ssh_user, ssh_key)

# Run command and save output to the variable
ls = ssh.run(["ls", "-latr", path("/mnt"], capture_output=True, check=True).stdout

# Mount directory
ssh.mount(source="storage:/data", "/mnt", force=True, mkdir=True)

# Remove files
ssh.remove("/my/folder/*.tar", force=True)

# Read text
text = ssh.read_text("/folder/text.txt")

# Write text
ssh.write_text("Hey!", "/folder/text.txt")

# Check if file
if ssh.isfile("/my/file):
    print("It's a file!")
```
