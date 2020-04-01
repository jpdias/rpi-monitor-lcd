# rpi-monitor-lcd
A script for displaying random stats in a LCD display (16x2 but works for others).


## Run as a Service

1. Set your username in the file `rpimonitorlcd.service` after `User=`
2. Set the path for the `script.py` in `rpimonitorlcd.service` after `ExecStart=`
3. Copy file `rpimonitorlcd.service` to `/etc/systemd/system/`
4. Run `systemctl deamon-reload`
5. Run `systemctl start rpimonitorlcd`
6. To add to boot run `systemctl enable rpimonitorlcd`

