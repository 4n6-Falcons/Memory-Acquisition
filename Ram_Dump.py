#!/usr/bin/env python
from sys import platform, exit
import subprocess
from os import makedirs, getcwd
from datetime import datetime
import config
import time

# get the current working directory
cwd = getcwd()
output = f"{cwd}\\Output\\"

def get_dump_file_path(filefmt_choice, specified_filename):
    """Create a file path with current date and time"""
    makedirs("Output", exist_ok=True)
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    filefmt_choice = ".raw" if filefmt_choice == "Default (.raw)" else filefmt_choice
    
    if specified_filename:
        file_name = specified_filename
    else:
        file_name = f"memdump_{current_time}"
        
    file_path = output + file_name + filefmt_choice#File path with date and time stamp
    return file_path

def detect_os():
    """Detect the current operating system"""
    global command
    if platform.startswith('win'):
        command = ['./tools/winpmem_mini_x64_rc2.exe']
        return 'Windows'
    elif platform.startswith('linux'):
        command = ['./tools/avml-minimal']
        return 'Linux'
    elif platform.startswith('darwin'):
        command = None
        return 'Mac OS'
    else:
        raise OSError("Unsupported operating system")
    
os_name = detect_os()
    
def dump_ram(file_path):
    """Dump the contents of RAM to a file."""
    process = subprocess.Popen(command + [file_path])

    while process.poll() is None:
        if config.reset:
            process.kill()
        time.sleep(0.1)


if __name__ == "__main__":
    dump_ram(config.file_path)