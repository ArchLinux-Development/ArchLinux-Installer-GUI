import subprocess

def install_kde_plasma():
    try:
        subprocess.run(['pacman', '-S', 'plasma', '--noconfirm'], check=True)
        return "KDE Plasma installed successfully"
    except subprocess.CalledProcessError as e:
        return f"Error installing KDE Plasma: {e}"
