#!/bin/sh
echo "===================================================================="
echo "Welcome to the setup. This will set up the local virtual environment."
echo "And then it will install all the required Python libraries."
echo "You can rerun this without any issues."
echo "===================================================================="

# Check if .env folder exists
if [ -d ".env" ]; then
    echo "Enabling virtual env"
else
    echo "No virtual env. Please run setup.sh first"
    exit 1  # Use exit code 1 to indicate an error
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

# Set environment variable (you can customize this)
export ENV=development
echo "Please enter your Gemini API Key:"
read -r GOOGLE_API_KEY
export GOOGLE_API_KEY=$GOOGLE_API_KEY

# Run your Python script (modify 'main.py' as needed)
python3 main.py

# Deactivate the virtual environment

if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
    # Linux or macOS
    deactivate
elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" ]]; then
    # Cygwin (POSIX compatibility layer for Windows) or MSYS (Git Bash)
    .env/Scripts/deactivate.bat
fi