import subprocess

def install_systemd_boot():
    try:
        subprocess.run(['bootctl', 'install'], check=True)
        return "systemd-boot installed successfully"
    except subprocess.CalledProcessError as e:
        return f"Error installing systemd-boot: {e}"
