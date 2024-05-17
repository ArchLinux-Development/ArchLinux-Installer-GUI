import subprocess

def install_enlightenment():
    try:
        subprocess.run(['pacman', '-S', 'enlightenment', '--noconfirm'], check=True)
        return "Enlightenment installed successfully"
    except subprocess.CalledProcessError as e:
        return f"Error installing Enlightenment: {e}"
