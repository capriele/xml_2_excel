#!/bin/bash

set -e

# Get the latest tag
VERSION=$1

# Get the commit hash corresponding to the latest tag
COMMIT=$2

# Output version and commit for debugging purposes
echo "VERSION=${VERSION}"
echo "COMMIT=${COMMIT}"

# Replace version and commit in dbng.py (or your main script)
sed -i "s/__VERSION__/${VERSION}/g" main.py
sed -i "s/__COMMIT__/${COMMIT}/g" main.py

# Build the project for Linux using PyInstaller
echo "Building for Linux..."
pip install -r requirements.txt
pyinstaller -F -w -n main main.py

# Package binaries into a zip file
echo "Packaging binaries..."
mkdir -p wheels
pip download --dest wheels -r requirements.txt
zip -r dist/binaries_linux.zip wheels

# Output the result
echo "Build complete. Check 'dist' directory."
