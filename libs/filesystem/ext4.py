import subprocess

def setup_ext4():
    try:
        # Example command for setting up ext4 on /dev/sdX1 (replace with actual device)
        subprocess.run(['mkfs.ext4', '/dev/sdX1'], check=True)
        return "ext4 filesystem setup successfully"
    except subprocess.CalledProcessError as e:
        return f"Error setting up ext4 filesystem: {e}"
