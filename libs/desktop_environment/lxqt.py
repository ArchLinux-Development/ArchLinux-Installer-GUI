import subprocess

def install_lxqt():
    try:
        subprocess.run(['pacman', '-S', 'lxqt', '--noconfirm'], check=True)
        return "LXQt installed successfully"
    except subprocess.CalledProcessError as e:
        return f"Error installing LXQt: {e}"
