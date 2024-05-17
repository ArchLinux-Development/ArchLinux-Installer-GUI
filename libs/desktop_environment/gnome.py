import subprocess

def install_gnome():
    try:
        subprocess.run(['pacman', '-S', 'gnome', '--noconfirm'], check=True)
        return "GNOME installed successfully"
    except subprocess.CalledProcessError as e:
        return f"Error installing GNOME: {e}"
