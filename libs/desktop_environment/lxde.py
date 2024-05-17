import subprocess

def install_lxde():
    try:
        subprocess.run(['pacman', '-S', 'lxde', '--noconfirm'], check=True)
        return "LXDE installed successfully"
    except subprocess.CalledProcessError as e:
        return f"Error installing LXDE: {e}"
