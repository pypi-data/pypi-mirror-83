import os
import socket
import subprocess
import logging
import shutil

from . import config

def _read_file(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'r') as info_file:
        return info_file.read().strip()

def get_machine_id():
    return _read_file('/etc/machine-id')

def get_serial():
    # Extract serial from cpuinfo file
    with open(config.PROC_PATH + '/cpuinfo', 'r') as cpuinfo_file:
        for line in cpuinfo_file:
            if line[0:6] == 'Serial':
                return line[10:26]
    return "0000000000000000"

def get_hostname():
    return socket.gethostname()

def get_local_ip():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.settimeout(5)
    client.connect(("8.8.8.8", 53))
    local_ip = client.getsockname()[0]
    client.close()
    return local_ip

def get_macs():
    result = []
    root_dir = config.SYS_PATH + '/class/net'
    interfaces = os.listdir(root_dir)
    for interface in interfaces:
        if interface == 'lo' or interface.startswith('br') or interface.startswith('docker') or interface.startswith('veth'):
            continue
        with open(os.path.join(root_dir, interface, 'address'), 'r') as interface_file:
            result.append({'name': interface, 'address': interface_file.read().strip()})
    return result

def get_ssid():
    if shutil.which('iwgetid') is None:
        return None
    try:
        ssid = subprocess.check_output('iwgetid -r', shell=True)
    except subprocess.CalledProcessError:
        return None
    return ssid.decode().strip()

def get_temp():
    temp_file_content = _read_file(config.SYS_PATH + '/class/thermal/thermal_zone0/temp')
    if not temp_file_content:
        return None
    temp_raw = int(temp_file_content)
    temp = float(temp_raw / 1000.0)
    return temp

def get_cpu_frequency():
    return int(_read_file(config.SYS_PATH + '/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq'))

def get_signal_level():
    wireless_data = _read_file(config.PROC_PATH + '/net/wireless')
    lines = wireless_data.split("\n")
    if len(lines) < 3:
        return None
    last_line = lines[-1]
    values = last_line.split()
    if len(values) < 4:
        return None
    return int(float(values[3]))

def get_written_kbytes():
    device_path = config.SYS_PATH + '/fs/ext4/mmcblk0p2'
    stat_files = ['session_write_kbytes', 'lifetime_write_kbytes']
    data = None
    for stat_file in stat_files:
        written = _read_file(os.path.join(device_path, stat_file))
        if written:
            data = {} if not data else data
            data[stat_file.split('_')[0]] = int(written)
    return data

def get_uptime():
    uptime_data = _read_file(config.PROC_PATH + '/uptime')
    return float(uptime_data.split()[0])

def get_kernel():
    return {
        'release': _read_file(config.PROC_PATH + '/sys/kernel/osrelease'),
        'version': _read_file(config.PROC_PATH + '/sys/kernel/version'),
    }

def save_secret(secret):
    path = config.SECRET_PATH
    base_path = os.path.dirname(path)

    try:
        os.makedirs(base_path, exist_ok=True)
    except PermissionError as err:
        logging.warning(err)
        return False

    with open(path, 'w') as secret_file:
        secret_file.write(secret)
        return True

def load_secret():
    path = config.SECRET_PATH
    try:
        with open(path, 'r') as secret_file:
            secret = secret_file.read()
            return secret.strip()
    except FileNotFoundError as err:
        logging.error(err)
        return None
