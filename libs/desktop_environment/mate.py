import subprocess

def install_mate():
    try:
        subprocess.run(['pacman', '-S', 'mate', 'mate-extra', '--noconfirm'], check=True)
        return "MATE installed successfully"
    except subprocess.CalledProcessError as e:
        return f"Error installing MATE: {e}"
