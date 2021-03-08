import os
import re

BOOTTIME_THRESHOLD = 1800 # seconds
SYSTEMLOAD_THRESHOLD = 1

boot_time = os.popen("cat /proc/uptime").read().strip().split(' ')
if (float(boot_time[0]) < BOOTTIME_THRESHOLD):
    print("Just booted {} min\nExit process".format(round(float(boot_time[0]) / 60)))
    exit(0)

uptime_resp = os.popen("uptime").read()
uptime_resp = re.findall(r"load average\:\s?([\d\.]+),\s?([\d\.]+),\s?([\d\.]+)", uptime_resp)
if len(uptime_resp) > 0:
    uptime15 = uptime_resp[0][2]
    if float(uptime15.strip()) < SYSTEMLOAD_THRESHOLD:
        print("Idle")
        loginstats = os.popen("last").read().split("\n")
        for i in loginstats:
            if re.match(".*still logged in.*", i):
                print("Detected active user(s)\nExit process")
                exit(0)
            else:
                print(i)

        print("No user active\nSHUTDOWN NOW")
        os.system("shutdown now")
else:
    print("Obtain system load failed")
    exit(1)