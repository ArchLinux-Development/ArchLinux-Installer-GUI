import subprocess

def install_refind():
    try:
        subprocess.run(['pacman', '-S', 'refind', '--noconfirm'], check=True)
        subprocess.run(['refind-install'], check=True)
        return "rEFInd installed successfully"
    except subprocess.CalledProcessError as e:
        return f"Error installing rEFInd: {e}"
