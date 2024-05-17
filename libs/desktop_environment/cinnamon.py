import subprocess

def install_cinnamon():
    try:
        subprocess.run(['pacman', '-S', 'cinnamon', '--noconfirm'], check=True)
        return "Cinnamon installed successfully"
    except subprocess.CalledProcessError as e:
        return f"Error installing Cinnamon: {e}"
