#!/bin/bash

# Update package list and install dependencies
sudo apt update
sudo apt install -y make gcc perl git

# Clone the ExifTool repository
git clone https://github.com/exiftool/exiftool.git

# Change directory to the cloned repository
cd exiftool

# Make and install ExifTool
perl Makefile.PL
make
sudo make install

echo "ExifTool installation completed successfully!"

















	
