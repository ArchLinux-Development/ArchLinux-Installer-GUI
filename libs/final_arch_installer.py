import os
import subprocess


def is_inside_chroot():
    return os.path.exists("/etc/arch-release") and not os.path.exists("/proc/1/root")

def run_command(command):
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, universal_newlines=True)
        
        output_lines = []
        for line in process.stdout:
            print(line, end='')  # Stream to stdout (which will be intercepted)
            output_lines.append(line)
            
        process.wait()
        
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, command, "".join(output_lines))
            
        # Mock result object for compatibility if needed, or just return stdout string
        class MockResult:
            def __init__(self, stdout):
                self.stdout = stdout
                
        return MockResult("".join(output_lines))

    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        return None

def run_chaotic_aur_setup():
    print("Setting up Chaotic-AUR inside chroot environment...")
    if not is_inside_chroot():
        print("You are not inside the chroot environment. Please chroot into the system first.")
        return
    run_command("pacman-key --recv-key 3056513887B78AEB --keyserver keyserver.ubuntu.com")
    run_command("pacman-key --lsign-key 3056513887B78AEB")
    run_command("pacman -U 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-keyring.pkg.tar.zst' 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-mirrorlist.pkg.tar.zst'")
    run_command('echo -e "\n[chaotic-aur]\nInclude = /etc/pacman.d/chaotic-mirrorlist" >> /etc/pacman.conf')
    print("Chaotic-AUR setup complete!")

def run_cachyos_repo_setup():
    print("Setting up CachyOS repository inside chroot environment...")
    if not is_inside_chroot():
        print("You are not inside the chroot environment. Please chroot into the system first.")
        return
    run_command("pacman-key --recv-keys F3B607488DB35A47 --keyserver keyserver.ubuntu.com")
    run_command("pacman-key --lsign-key F3B607488DB35A47")
    run_command("pacman -U 'https://mirror.cachyos.org/repo/x86_64/cachyos/cachyos-keyring-3-1-any.pkg.tar.zst' 'https://mirror.cachyos.org/repo/x86_64/cachyos/cachyos-mirrorlist-17-1-any.pkg.tar.zst' 'https://mirror.cachyos.org/repo/x86_64/cachyos/cachyos-v3-mirrorlist-17-1-any.pkg.tar.zst' 'https://mirror.cachyos.org/repo/x86_64/cachyos/cachyos-v4-mirrorlist-5-1-any.pkg.tar.zst' 'https://mirror.cachyos.org/repo/x86_64/cachyos/pacman-6.0.2-13-x86_64.pkg.tar.zst'")

    cpu_compatibility = run_command("/lib/ld-linux-x86-64.so.2 --help | grep supported | grep x86-64-v4")
    if "supported, searched" in cpu_compatibility.stdout:
        run_command('echo -e "\n[cachyos-v4]\nInclude = /etc/pacman.d/cachyos-v4-mirrorlist" >> /etc/pacman.conf')

    cpu_compatibility_v3 = run_command("/lib/ld-linux-x86-64.so.2 --help | grep supported | grep x86-64-v3")
    if "supported, searched" in cpu_compatibility_v3.stdout:
        run_command('echo -e "\n[cachyos-v3]\nInclude = /etc/pacman.d/cachyos-v3-mirrorlist" >> /etc/pacman.conf')
        run_command('echo -e "\n[cachyos-core-v3]\nInclude = /etc/pacman.d/cachyos-v3-mirrorlist" >> /etc/pacman.conf')
        run_command('echo -e "\n[cachyos-extra-v3]\nInclude = /etc/pacman.d/cachyos-v3-mirrorlist" >> /etc/pacman.conf')

    run_command('echo -e "\n[cachyos]\nInclude = /etc/pacman.d/cachyos-mirrorlist" >> /etc/pacman.conf')
    print("CachyOS repository setup complete!")

def create_filesystem(fs_type, device):
    try:
        print(f"Creating {fs_type} filesystem on {device}...")
        if fs_type == "ext4":
            run_command(f"mkfs.ext4 -F {device}") # -F to force
        elif fs_type == "btrfs":
            run_command(f"mkfs.btrfs -f {device}") # -f to force
        elif fs_type == "zfs":
            run_command(f"zpool create -f mypool {device}")
        elif fs_type == "xfs":
            run_command(f"mkfs.xfs -f {device}")
        elif fs_type == "jfs":
            run_command(f"mkfs.jfs -q {device}")
        elif fs_type == "reiserfs":
            run_command(f"mkfs.reiserfs -f {device}")
        elif fs_type == "f2fs":
            run_command(f"mkfs.f2fs -f {device}")
        else:
            print(f"Error: Unknown filesystem type: {fs_type}")
            return

        print(f"Filesystem {fs_type} created successfully on {device}.")
    except Exception as e:
        print(f"Failed to create filesystem: {e}")
        raise e

def install_microcode():
    # Detect the CPU vendor
    cpu_vendor = run_command("grep -m 1 'vendor_id' /proc/cpuinfo").stdout

    if "Intel" in cpu_vendor:
        print("Intel CPU detected. Installing intel-ucode...")
        run_command("pacman -S intel-ucode")
    elif "AMD" in cpu_vendor:
        print("AMD CPU detected. Installing amd-ucode...")
        run_command("pacman -S amd-ucode")
    else:
        print("Unknown CPU vendor. Skipping microcode installation.")
