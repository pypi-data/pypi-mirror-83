# SNX Tray
Tray Icon for snx

## Install 
``pip install snxtray``

##### Ubuntu 18.04 LTS wx build dependencies:

``make gcc libgtk-3-dev libwebkitgtk-dev libwebkitgtk-3.0-dev libgstreamer-gl1.0-0 freeglut3 freeglut3-dev python-gst-1.0 python3-gst-1.0 libglib2.0-dev ubuntu-restricted-extras libgstreamer-plugins-base1.0-dev``

## Configuration 
#### Example config
`cat $HOME/.config/snxtray.json`
```json
{
  "server": "IP/URL",
  "cert": "path to cert",
  "keep_passwd": false,
  "elevate": "pkexec",
  "post-up": [["exsample", "-u"]],
  "post-down": [["exsample", "-d", "arg2"]]
}
```
**Note: if `elevate` is not set to `hooks` this string is added as an prefix to the snx command**
`post-up/down` are optional
#### Use root Hooks
To use root Hooks you need to configure your snxtray with `cert`, `server` and set `elevate` to `hooks`.<br>
Then you can run `sudo -E snxtray --init-hooks` this create the file structure in */etc/snxtray* and configures the up hook
with the values of your config **Note: all users that use hooks will use the same configuration**

You now can edit the post-down and post-up to call commands with root permissions



