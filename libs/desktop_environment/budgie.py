import subprocess

def install_budgie():
    try:
        subprocess.run(['pacman', '-S', 'budgie-desktop', '--noconfirm'], check=True)
        return "Budgie installed successfully"
    except subprocess.CalledProcessError as e:
        return f"Error installing Budgie: {e}"
