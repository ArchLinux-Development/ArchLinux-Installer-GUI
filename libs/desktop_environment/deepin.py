import subprocess

def install_deepin():
    try:
        subprocess.run(['pacman', '-S', 'deepin', '--noconfirm'], check=True)
        return "Deepin installed successfully"
    except subprocess.CalledProcessError as e:
        return f"Error installing Deepin: {e}"
