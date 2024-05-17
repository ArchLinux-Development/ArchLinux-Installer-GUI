import subprocess

def setup_reiserfs():
    try:
        # Example command for setting up reiserfs on /dev/sdX1 (replace with actual device)
        subprocess.run(['mkfs.reiserfs', '/dev/sdX1'], check=True)
        return "ReiserFS filesystem setup successfully"
    except subprocess.CalledProcessError as e:
        return f"Error setting up ReiserFS filesystem: {e}"
