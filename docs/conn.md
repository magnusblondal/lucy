## Remote server
Til ad tengjast DO þarf ad skrá ssh lykill hjá þeim

Tengist med ssh root@x.x.x.x

Create user

Copy keys into ssh folder -> þetta er lykillinn sem github notar til ad tengjast
```
cat id_[...] | ssh user@x.x.x.x 'cat >> .ssh/id_[...]'
cat id_[...].pub | ssh user@x.x.x.x 'cat >> .ssh/id_[...].pub'
```
Copy .pub key into 'authorized_keys'
```
cat id_[...].pub | ssh user@x.x.x.x 'cat >> .ssh/authorized_keys'
```
Clone source
```
su [user]
git clone git@github.com:magnusblondal/lucy.git
```


## Þegar Droplet er búinn til
In the Advanced Options section, additionally check the box for user data. In the text box that opens, copy and paste the following script. This script will create a new sudo user, copy your public ssh key to that new user's authorized_keys file, and disable ssh root logins.
```
#!/bin/bash
set -euo pipefail

USERNAME=XXXXXX # TODO: Customize the sudo non-root username here

# Create user and immediately expire password to force a change on login
useradd --create-home --shell "/bin/bash" --groups sudo "${USERNAME}"
passwd --delete "${USERNAME}"
chage --lastday 0 "${USERNAME}"

# Create SSH directory for sudo user and move keys over
home_directory="$(eval echo ~${USERNAME})"
mkdir --parents "${home_directory}/.ssh"
cp /root/.ssh/authorized_keys "${home_directory}/.ssh"
chmod 0700 "${home_directory}/.ssh"
chmod 0600 "${home_directory}/.ssh/authorized_keys"
chown --recursive "${USERNAME}":"${USERNAME}" "${home_directory}/.ssh"

# Disable root SSH login with password
sed --in-place 's/^PermitRootLogin.*/PermitRootLogin prohibit-password/g' /etc/ssh/sshd_config
if sshd -t -q; then systemctl restart sshd; fi 
```
