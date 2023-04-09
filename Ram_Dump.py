#!/usr/bin/env python
from sys import platform, exit
#from subprocess import Popen
from subprocess import run #Using run method for better RAM Management
from os import path, makedirs, getcwd

# get the current working directory
cwd = getcwd()

def dump_ram():
    # create the "Output" folder if it doesn't exist
    if not path.exists("Output"):
        makedirs("Output")
    # create a file path relative to the current working directory
    file_path = path.join(cwd, "Output/mem.raw")
        
    # Check the current operating system
    if platform.startswith('win'):
        # Execute the Windows RAM dump code
        """process = Popen(['./tools/winpmem_mini_x64_rc2.exe', file_path])
        process.wait()"""
        run(['./tools/winpmem_mini_x64_rc2.exe', file_path], check=True)
        
    elif platform.startswith('linux'):
        # Execute the Linux RAM dump code
        """process = Popen(['./tools/avml-minimal', file_path])
        process.wait()"""
        run(['./tools/avml-minimal', file_path], check=True)
        
    elif platform.startswith('darwin'):
        # Execute the Mac RAM dump code
        pass
    
    else:
        print("Unsupported operating system")
        exit(1)

def main():
    # Start the process to collect the RAM dump
    print("Starting RAM dump collection...")
    dump_ram()
    print("RAM dump saved")

if __name__ == "__main__":
    main()
