import subprocess

def setup_ext4(device):
    try:
        subprocess.run(['mkfs.ext4', device], check=True)
        return "ext4 filesystem setup successfully"
    except subprocess.CalledProcessError as e:
        return f"Error setting up ext4 filesystem: {e}"
