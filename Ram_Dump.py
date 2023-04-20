#!/usr/bin/env python
import sys
import subprocess
import os
from datetime import datetime
import time
import psutil
import platform
import hashlib
import socket
import wmi

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
    global file_name
    global formatted_date
    """Create a file path with current date and time"""
    os.makedirs("Output", exist_ok=True)
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    formatted_date = datetime.now().strftime("%A %d %B %Y %H:%M:%S")

    filefmt_choice = ".raw" if filefmt_choice == "Default (.raw)" else filefmt_choice

    if specified_filename:
        file_name = specified_filename
    else:
        file_name = f"memdump_{current_time}"

    # File path with date and time stamp
    file_path = output + file_name + filefmt_choice
    return file_path


os_name = detect_os()
print(command)


def dump_ram(file_path):
    """Dump the contents of RAM to a file."""
    process = subprocess.Popen(
        command + [file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startupinfo)

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

# Insert your report creation function here
elapsed_time = ""
end_time = ""


def generate_report(filefmt_choice):
    os.makedirs("Output", exist_ok=True)
    open(f'Output/{file_name}_report.txt', 'w').write('')
    with open(file_path, "rb") as f:
        contents = f.read()
        md5_hash = hashlib.md5(contents).hexdigest()
        sha1_hash = hashlib.sha1(contents).hexdigest()
        sha256_hash = hashlib.sha256(contents).hexdigest()

    system_id = platform.node()
    system_manufacturer = platform.system()

    system_architecture = platform.architecture()[0]

    os_name = platform.system()
    os_version = platform.version()
    os_build = platform.platform()

    installed_memory = f"{psutil.virtual_memory().available / 1024**3:.2f} GB"
    total_physical_memory = f"{psutil.virtual_memory().total / 1024**3:.2f} GB"
    total_virtual_memory = f"{psutil.swap_memory().total / 1024**3:.2f} GB"
    report_template = """
--------------xx Memory Acquisition Report xx--------------
Report Created By 4n6 Memory Acquisition Tool v1.0
-----------------------------------------------------------

[Case Details:]
    Number:      {case_number}
    Name:        {case_name}
    Description: {case_description}
    
[Examiner Details:]
    Name:         {examiner_name}
    Phone No.:    {examiner_phone}
    Email Id:     {examiner_email}
    Organization: {examiner_organization}

-----------------------------------------------------------

[Dump File Information:]

	File Name: {file_name}
	File Format: {specified_file_format}
	File Size: {file_size} GB
	File Location: {file_path}

	MD5 Hash: {md5_hash}
	SHA1 Hash: {sha1_hash}
	SHA256 Hash: {sha256_hash}

-----------------------------------------------------------

[Acquisition Details:]
	
	Start Time: {current_time}
	End Time: {end_time}
	Elapsed Time: {elapsed_time}

-----------------------------------------------------------

[Target Device Information:]

    System Name: {system_name}
    System Id: {system_id}
    System Manufacturer: {system_manufacturer}
    System Model: {system_model}
    System Architecture: {system_architecture}

    OS Name: {os_name}
    OS Version: {os_version}
    OS Build: {os_build}

    Installed Physical Memory (RAM) : {installed_memory}
    Total Physical Memory: {total_physical_memory}
    Total Virtual Memory: {total_virtual_memory}

-----------------------------------------------------------
        """

    report = report_template.format(
        case_number=case_details["Case Number"],
        case_name=case_details["Case Name"],
        case_description=case_details["Case Description"],
        examiner_name=examiner_details["Name"],
        examiner_phone=examiner_details["Phone Number"],
        examiner_email=examiner_details["Email Id"],
        examiner_organization=examiner_details["Organization"],
        system_name=socket.gethostname(),
        system_id=system_id,
        system_manufacturer=system_manufacturer,
        system_model=wmi.WMI().Win32_ComputerSystem()[0].Model,
        system_architecture=system_architecture,
        os_name=os_name,
        os_version=os_version,
        os_build=os_build,
        installed_memory=installed_memory,
        total_physical_memory=total_physical_memory,
        total_virtual_memory=total_virtual_memory,
        file_name=file_name,
        file_path=file_path,
        specified_file_format=filefmt_choice,
        file_size=(os.path.getsize(file_path)/1024 ** 3),
        md5_hash=md5_hash,
        sha1_hash=sha1_hash,
        sha256_hash=sha256_hash,
        current_time=formatted_date,
        end_time=end_time,
        elapsed_time=elapsed_time,
    )

    with open(f"Output/{file_name}_report.txt", "w") as f:
        f.write(report)


if __name__ == "__main__":
    dump_ram(file_path)
