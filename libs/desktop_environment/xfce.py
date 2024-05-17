import subprocess

def install_xfce():
    try:
        subprocess.run(['pacman', '-S', 'xfce4', 'xfce4-goodies', '--noconfirm'], check=True)
        return "Xfce installed successfully"
    except subprocess.CalledProcessError as e:
        return f"Error installing Xfce: {e}"
