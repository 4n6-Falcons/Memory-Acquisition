#!/usr/bin/env python
import sys
import subprocess
import os
from datetime import datetime
import time

# get the current working directory
cwd = os.getcwd()
output = f"{cwd}/Output/"

reset = False
file_path = ""

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def detect_os():
    """Detect the current operating system"""
    global startupinfo
    global command
    if sys.platform.startswith('win'):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        command = [resource_path('tools/winpmem_mini_x64_rc2.exe')]
        return 'Windows'
    elif sys.platform.startswith('linux'):
        startupinfo = None
        command = ['./tools/avml-minimal']
        return 'Linux'
    elif sys.platform.startswith('darwin'):
        startupinfo = None
        command = None
        return 'Mac OS'
    else:
        raise OSError("Unsupported operating system")

def get_dump_file_path(filefmt_choice, specified_filename):
    """Create a file path with current date and time"""
    os.makedirs("Output", exist_ok=True)
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    filefmt_choice = ".raw" if filefmt_choice == "Default (.raw)" else filefmt_choice
    
    if specified_filename:
        file_name = specified_filename
    else:
        file_name = f"memdump_{current_time}"
        
    file_path = output + file_name + filefmt_choice#File path with date and time stamp
    return file_path

os_name = detect_os()
print(command)
    
def dump_ram(file_path):
    """Dump the contents of RAM to a file."""
    process = subprocess.Popen(command + [file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startupinfo)

    while process.poll() is None:
        if reset:
            process.kill()
        time.sleep(0.1)

# Labels and entries for Case Details
case_details = {
    "Case Number": "",
    "Case Name": "",
    "Case Description": ""
}

# Labels and entries for Examiner Details
examiner_details = {
    "Name": "",
    "Phone Number": "",
    "Email Id": "",
    "Organization": ""
}

elapsed_time = ""
end_time = ""

# Insert your report creation function here

if __name__ == "__main__":
    dump_ram(file_path)