import I2C_LCD_driver
import socket
import fcntl
import struct
import psutil
import datetime
import time
import random
import os, sys
from daemonize import Daemonize
from subprocess import PIPE, Popen

pilcd = I2C_LCD_driver.lcd(0x3f)

lcd_number_of_lines = 2
lcd_size_of_row = 16

def set_lcd_line(line, msg):
    #max 16 chars
    if(len(msg) > lcd_size_of_row):
        raise Exception("Line lenght max size of 16")
    pilcd.lcd_display_string(msg, line)
    return 0

def get_ip_address(wifi = False):
    #wifi or eth
    ip = psutil.net_if_addrs()["eth0"][0].address
    if(wifi):
        ip = psutil.net_if_addrs()["wlan0"][0].address
        return "wl {:>12}".format(ip)
    return "et {:>12}".format(ip)

def uptime():
    uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(round(psutil.boot_time()))
    uptimedays = uptime.days
    return "uptime {:>8}d".format(uptimedays)

def last_reboot():
    firsttimestamp = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%d/%m/%y")
    return "boot {:>11}".format(firsttimestamp)

def get_cpu_temperature():
    temp = psutil.sensors_temperatures()["cpu-thermal"][0].current;
    return "CPU Temp {0:>5.1f} C".format(temp)

def get_ram_usage():
    # vmem(total=8589934592L, available=4073336832L, percent=52.6, used=5022085120L, free=3560255488L, active=2817949696L, inactive=513081344L, wired=1691054080L)
    total = psutil.virtual_memory().total/1024/1024
    used = psutil.virtual_memory().used/1024/1024
    percent = psutil.virtual_memory().percent
    return "RAM {0:6.2f} {1:>4.1f}%".format(total, percent)

def get_cpu_usage():
    current_usage = psutil.cpu_percent(interval=None)
    max_usage = psutil.cpu_freq().max/1000 #GHz
    return "CPU {0:6.2f} {1:>4.1f}%".format(max_usage, current_usage)

def get_disk_usage():
    total = psutil.disk_usage('/').total/1024/1024
    used = psutil.disk_usage('/').used/1024/1024
    percent = psutil.disk_usage('/').percent
    return "SDc {0:6.2f} {1:>4.1f}%".format(total, percent)

stats = [get_ip_address, uptime, last_reboot, get_cpu_temperature, get_ram_usage, get_cpu_usage, get_disk_usage]

def fill_screen():
    picked = []
    while len(picked) != 2:
        res = random.choice(stats)
        if not any(elem == res for elem in picked):
            picked.append(res)

    for i in range(len(picked)):
        set_lcd_line(i+1, picked[i]())

        
def main():
    while(True):
        fill_screen()
        time.sleep(30)


if __name__ == '__main__':
        myname=os.path.basename(sys.argv[0])
        pidfile='/tmp/%s' % myname       # any name
        daemon = Daemonize(app=myname,pid=pidfile, action=main)
        daemon.start()