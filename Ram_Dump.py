#!/usr/bin/env python
from sys import platform, exit
from subprocess import Popen
from os import makedirs, getcwd
from datetime import datetime
import config
import time

# get the current working directory
cwd = getcwd()
output = f"{cwd}\\Output\\"
OS = platform

def get_dump_file_path():
    """Create a file path with current date and time"""
    makedirs("Output", exist_ok=True)
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"memdump_{current_time}.raw"
    file_path = output + file_name #File path with date and time stamp
    return file_path

def dump_ram(file_path):
    """Dump the Contents of Ram to a file"""
    # Check the current operating system
    if OS.startswith('win'):
        # Execute the Windows RAM dump code
        process = Popen(['./tools/winpmem_mini_x64_rc2.exe', file_path])
        
    elif OS.startswith('linux'):
        # Execute the Linux RAM dump code
        process = Popen(['./tools/avml-minimal', file_path], check=True)
        
    elif OS.startswith('darwin'):
        # Execute the Mac RAM dump code
        pass
    
    else:
        print("Unsupported operating system")
        exit(1)

    while process.poll() is None:
        if config.reset:
            process.kill()
        time.sleep(0.1)


if __name__ == "__main__":
    dump_ram(config.file_path)