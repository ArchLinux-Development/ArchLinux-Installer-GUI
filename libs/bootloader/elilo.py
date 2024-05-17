import subprocess

def install_elilo():
    try:
        subprocess.run(['pacman', '-S', 'elilo', '--noconfirm'], check=True)
        subprocess.run(['elilo'], check=True)
        return "Elilo installed successfully"
    except subprocess.CalledProcessError as e:
        return f"Error installing Elilo: {e}"
