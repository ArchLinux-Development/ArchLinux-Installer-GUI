import subprocess

def install_grub():
    try:
        subprocess.run(['pacman', '-S', 'grub', '--noconfirm'], check=True)
        subprocess.run(['grub-install', '--target=i386-pc', '/dev/sdX'], check=True)  # Replace /dev/sdX with the actual target disk
        subprocess.run(['grub-mkconfig', '-o', '/boot/grub/grub.cfg'], check=True)
        return "GRUB installed successfully"
    except subprocess.CalledProcessError as e:
        return f"Error installing GRUB: {e}"
