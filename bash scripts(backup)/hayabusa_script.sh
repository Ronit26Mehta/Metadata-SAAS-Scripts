#!/bin/bash

# Update package list and install dependencies
sudo apt update
sudo apt install -y git python3 python3-pip

# Clone the Hayabusa repository
git clone https://github.com/Yamato-Security/hayabusa.git

# Change directory to the cloned repository
cd hayabusa

# Install Hayabusa dependencies
pip3 install -r requirements.txt

echo "Hayabusa installation completed successfully!"

