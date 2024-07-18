#!/bin/sh
echo "===================================================================="
echo "Welcome to to the setup. This will setup the local virtual env. "
echo "And then it will install all the required python libraries. "
echo "You can rerun this without any issues. "
echo "===================================================================="

# Check if .env folder exists
if [ -d ".env" ]; then
    echo ".env folder exists. Installing using pip"
else
    echo "creating .env and install using pip"
    python3 -m venv .env
fi

# Activate virtual environment (corss-platform)

if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
    # Linux or macOS
    source .env/bin/activate
elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" ]]; then
    # Cygwin (POSIX compatibility layer for Windows) or MSYS (Git Bash)
    .env/Scripts/activate.bat
else
    echo "Unsupported operating system. Please activate the virtual environment manually."
fi

# Upgrade the pip
pip install --upgrade pip

# Install required packages
pip install -r requirements.txt

# Deactivate the virtual environment

if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
    # Linux or macOS
    deactivate
elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" ]]; then
    # Cygwin (POSIX compatibility layer for Windows) or MSYS (Git Bash)
    .env/Scripts/deactivate.bat
fi