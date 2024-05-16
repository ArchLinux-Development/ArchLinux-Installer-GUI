#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Function to display messages
display_message() {
    echo
    echo "#################################################"
    echo "# $1"
    echo "#################################################"
    echo
}

# Display initial message
display_message "Welcome to the Arch Linux Initial Installer"

# Confirm if the user wants to proceed
read -p "This script will set up the environment, clone the Arch Linux Installer GUI repo, and run the installer. Do you want to proceed? (y/n): " confirm
if [[ $confirm != [yY] ]]; then
    echo "Installation aborted."
    exit 1
fi

# Update system and install git if not already installed
display_message "Updating system and installing git..."
sudo pacman -Syu --noconfirm
sudo pacman -S git --noconfirm

# Clone the git repository
REPO_URL="https://github.com/ArchLinux-Development/ArchLinux-Installer-GUI.git"
CLONE_DIR="/opt/ArchLinux-Installer-GUI"

display_message "Cloning repository from $REPO_URL..."
git clone $REPO_URL $CLONE_DIR

# Change into the cloned repository directory
cd $CLONE_DIR

# Confirm if the user wants to run the GUI installer
display_message "Repository cloned successfully."
read -p "Do you want to run the Arch Linux Installer GUI now? (y/n): " run_gui
if [[ $run_gui != [yY] ]]; then
    echo "You can run the installer later by navigating to $CLONE_DIR and executing the main Python script."
    exit 0
fi

# Run the main Arch Installer Python script
PYTHON_INSTALLER="main_installer.py"

display_message "Running the main Arch Installer GUI Python script..."
python $PYTHON_INSTALLER

display_message "Installation and setup complete."
