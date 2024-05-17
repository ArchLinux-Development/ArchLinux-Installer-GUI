import subprocess

def install_syslinux():
    try:
        subprocess.run(['pacman', '-S', 'syslinux', '--noconfirm'], check=True)
        subprocess.run(['syslinux-install_update', '-i', '-a', '-m'], check=True)
        return "Syslinux installed successfully"
    except subprocess.CalledProcessError as e:
        return f"Error installing Syslinux: {e}"
