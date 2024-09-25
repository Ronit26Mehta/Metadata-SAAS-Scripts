#!/bin/bash

is_installed() {
    python3 -c "import $1" &> /dev/null
}

HACHOIR_DIR="hachoir"

handle_error() {
    echo "Error: $1"
    echo "Setup failed."
    exit 1
}


if is_installed hachoir; then
    echo "Hachoir is already installed."
else
    echo "Cloning Hachoir repository..."
    git clone https://github.com/vstinner/hachoir.git "$HACHOIR_DIR" || handle_error "Failed to clone Hachoir repository"

    cd "$HACHOIR_DIR" || handle_error "Failed to navigate to Hachoir directory"

    echo "Upgrading setuptools..."
    pip install --upgrade setuptools || handle_error "Failed to upgrade setuptools"
    echo "Installing Hachoir..."
    pip install -e . || handle_error "Failed to install Hachoir"
fi

echo "Verifying installation..."
if  is_installed hachoir; then
    echo "installed"
else
    handle_error "Hachoir is not installed properly"
fi

pip install urwid || handle_error "not installed"
echo "installed urwid successfully"

