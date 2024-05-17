import subprocess

def install_lilo():
    try:
        subprocess.run(['pacman', '-S', 'lilo', '--noconfirm'], check=True)
        subprocess.run(['lilo'], check=True)
        return "LILO installed successfully"
    except subprocess.CalledProcessError as e:
        return f"Error installing LILO: {e}"
