'''
    |==================================|
    |  WifiLog v2.0 by HeladeraDragon  |
    |==================================|
    |                                  |
    |- https://heladeradragon.com.ar   |
    |                                  |
    |- Make sure to stop with Ctrl + C,|
    |  otherwise session data won't be |
    |  logged.                         |
    |                                  |
    |- It's a bit very buggy on small  |
    |  terminal sizes, feel free to PR |
    |  or smth, I'm done with this.    |
    |                                  |
    |- Run and go. This script requires|
    |  no setup. You can set it to     |
    |  launch on boot if you want      |
    |                                  |
    |- Logs network connections to a   |
    |  .log file called WifiLog.log,   |
    |  stored in the same directory as |
    |  the script's. This file can     |
    |  contain multiple sessions at the|
    |  same time.                      |
    |                                  |
    |- Only works on Windows set to    |
    |  English (check code if you want |
    |  to make it better)              |
    |                                  |
    |- Licensed under MIT because I    |
    |  hate GNU GPL with a passion.    |
    |                                  |
    |- Wish you luck in complaining    |
    |  with your ISP.                  |
    |                                  |
    |==================================|
'''

import subprocess
from datetime import datetime
import sys

# Pausable timer code from https://stackoverflow.com/a/60027719/
class MyTimer():
    def __init__(self):
        self.timestarted = None
        self.timepaused = None
        self.paused = False
    def start(self):
        self.timestarted = datetime.now()
    def pause(self):
        if self.timestarted is None:
            raise ValueError("Timer not started")
        if self.paused:
            return
        self.timepaused = datetime.now()
        self.paused = True
    def resume(self):
        if self.timestarted is None:
            raise ValueError("Timer not started")
        if not self.paused:
            return
        pausetime = datetime.now() - self.timepaused
        self.timestarted = self.timestarted + pausetime
        self.paused = False
    def get(self):
        if self.timestarted is None:
            raise ValueError("Timer not started")
        if self.paused:
            return self.timepaused - self.timestarted
        else:
            return datetime.now() - self.timestarted

def log_connection(status):
    with open("WifiLog.log", "a") as f:
        log_entry = f"{status}\n"
        f.write(log_entry)
        print(log_entry.strip())

def send_ping():
    try:
        subprocess.check_output(["ping", "-n", "1", "-l", "1", "-w"," 100", "1.1.1.1"])
        return True
    except subprocess.CalledProcessError:
        return False

def is_online():
    for _ in range(4):
        if(send_ping()):
            return True
    return False
    
def adapter_network_data():
    output = subprocess.run(["netsh", "wlan", "show", "interfaces"], capture_output=True, text=True)
    if output.returncode == 0:
        netstat = {
            'Radio type' : 'Not available',
            'SSID' : 'No network',
            'Band' : 'unknown',
            'Signal': 'unknown'
        }
        lines = output.stdout.split('\n')
        for line in lines:
            parts = line.split(':', 1)
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()
                netstat[key] = value
        return netstat
    else:
        print("Error: Unable to get network status.")
        return 

def network_eval():
    is_online_r = is_online()
    network_data = adapter_network_data()
    return {
        'Online'        : is_online_r,
        'Hardware'      : network_data['Name'],
        'NetworkAdapter': network_data['Description'],
        'Radio type'    : network_data['Radio type'],
        'SSID'          : network_data['SSID'],
        'Band'          : network_data['Band'],
        'Signal'        : network_data['Signal']
    }

def delete_last_lines(n=1):
    for _ in range(n):
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K")

uptime_stats = ""

def main():
    global uptime_stats
    prev_status = None
    normal_uptime = MyTimer()
    online_uptime = MyTimer()
    last_cut = datetime.now()

    interruptions = 0
    stat = network_eval()

    currentTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_connection("============== SESSION INFO =============")
    log_connection(f"|            Name: {stat['Hardware']}")
    log_connection(f"| Network adapter: {stat['NetworkAdapter']}")
    log_connection(f"|    Current time: {currentTime}")
    log_connection(f"| WifiLog version: v2.0")

    normal_uptime.start()
    online_uptime.start()
    
    if(stat['Online'] == False):
       online_uptime.pause()
       last_cut = datetime.now()

    print("")
    print("...")
    print("...")
    print("...")

    while True:
        currentTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        stat = network_eval()
        delete_last_lines(4)
        if stat['Online'] != prev_status:
            if stat['Online']:
                log_connection("| ")
                log_connection(f"|--------- {currentTime} ---------")
                log_connection(f"| INFO   Connected ({stat['SSID']} at {stat['Band']})")
                log_connection(f"|        Signal: {stat['Signal']}")
                last_cut = datetime.now()
                online_uptime.resume()
            else:
                log_connection("| ")
                log_connection(f"|--------- {currentTime} ---------")
                log_connection(f"| ERROR  Disconnected ({stat['SSID']})")
                if(stat['SSID'] != "No network"):
                    log_connection(f"|        Signal: {stat['Signal']}")
                online_uptime.pause()
                interruptions = interruptions + 1
            prev_status = stat['Online']

        if (stat['Online'] == False):
            last_cut = datetime(1, 1, 1)

        norm = normal_uptime.get()
        onli = online_uptime.get()
        last = datetime.now() - last_cut
        uptm = onli / norm * 100

        last_datetime = datetime(1, 1, 1) + last
        norm_datetime = datetime(1, 1, 1) + norm
        onli_datetime = datetime(1, 1, 1) + onli

        uptime_stats = f"""
Time online: {onli_datetime.strftime('%H:%M:%S')} | Session time: {norm_datetime.strftime('%H:%M:%S')}
Uptime: {round(uptm * 100) / 100}% | Interruptions: {interruptions}
Time since interruption: {last_datetime.strftime('%H:%M:%S')} """
        print(uptime_stats)
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        currentTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_connection("| INFO   Session ended by user")
        log_connection("============== SESSION END ==============")
        log_connection(f"|    Current time: {currentTime}")
        log_connection(f"{uptime_stats}")