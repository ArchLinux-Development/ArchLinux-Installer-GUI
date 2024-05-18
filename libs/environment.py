# libs/environment.py

import os
import subprocess

def is_virtual_environment():
    virtual_files = [
        "/sys/class/dmi/id/product_name",
        "/sys/class/dmi/id/sys_vendor",
        "/sys/class/dmi/id/board_vendor"
    ]

    virtual_keywords = ["VirtualBox", "VMware", "QEMU", "KVM", "Hyper-V", "Xen", "Bochs", "Parallels", "bhyve"]

    for file in virtual_files:
        if os.path.exists(file):
            with open(file, 'r') as f:
                content = f.read().lower()
                for keyword in virtual_keywords:
                    if keyword in content:
                        return True

    # Check using lscpu command
    try:
        result = subprocess.run(['lscpu'], stdout=subprocess.PIPE)
        output = result.stdout.decode('utf-8').lower()
        for keyword in virtual_keywords:
            if keyword in output:
                return True
    except Exception as e:
        print(f"Error checking lscpu: {e}")

    # Additional check using systemd-detect-virt
    try:
        result = subprocess.run(['systemd-detect-virt'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode('utf-8').strip().lower()
        if output and output != "none":
            return True
    except Exception as e:
        print(f"Error using systemd-detect-virt: {e}")

    return False
