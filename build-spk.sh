#!/bin/bash
#
# Build script for Streamlit Hub Synology Package
#
# Usage: ./build-spk.sh [version]
# Example: ./build-spk.sh 1.0.0
#

set -e

# Configuration
PACKAGE_NAME="streamlit-hub"
VERSION="${1:-1.0.0}"
BUILD_NUMBER="0001"
FULL_VERSION="${VERSION}-${BUILD_NUMBER}"

# Directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SPK_DIR="${SCRIPT_DIR}/spk"
BUILD_DIR="${SCRIPT_DIR}/build"
OUTPUT_DIR="${SCRIPT_DIR}/dist"

echo "==================================="
echo "Building Streamlit Hub SPK Package"
echo "Version: ${FULL_VERSION}"
echo "==================================="

# Clean previous build
rm -rf "${BUILD_DIR}"
mkdir -p "${BUILD_DIR}"
mkdir -p "${OUTPUT_DIR}"

# Create package directory structure
PACKAGE_BUILD="${BUILD_DIR}/package"
mkdir -p "${PACKAGE_BUILD}"

echo "Copying application files..."
# Copy application files to package
cp "${SCRIPT_DIR}/Dockerfile" "${PACKAGE_BUILD}/"
cp "${SCRIPT_DIR}/compose.yaml" "${PACKAGE_BUILD}/"
cp "${SCRIPT_DIR}/requirements.txt" "${PACKAGE_BUILD}/"
cp "${SCRIPT_DIR}/streamlit_app.py" "${PACKAGE_BUILD}/"
cp -r "${SCRIPT_DIR}/apps" "${PACKAGE_BUILD}/"

echo "Creating package.tgz..."
# Create package.tgz
cd "${PACKAGE_BUILD}"
tar czf "${BUILD_DIR}/package.tgz" .
cd "${SCRIPT_DIR}"

echo "Preparing SPK contents..."
# Prepare SPK directory
SPK_BUILD="${BUILD_DIR}/spk"
mkdir -p "${SPK_BUILD}"

# Copy INFO file and update version
cp "${SPK_DIR}/INFO" "${SPK_BUILD}/"
sed -i "s/version=.*/version=\"${FULL_VERSION}\"/" "${SPK_BUILD}/INFO"

# Copy icons
cp "${SPK_DIR}/PACKAGE_ICON.PNG" "${SPK_BUILD}/" 2>/dev/null || echo "Warning: PACKAGE_ICON.PNG not found"
cp "${SPK_DIR}/PACKAGE_ICON_256.PNG" "${SPK_BUILD}/" 2>/dev/null || echo "Warning: PACKAGE_ICON_256.PNG not found"

# Copy scripts and make executable
mkdir -p "${SPK_BUILD}/scripts"
cp "${SPK_DIR}/scripts/"* "${SPK_BUILD}/scripts/"
chmod +x "${SPK_BUILD}/scripts/"*

# Copy conf directory
if [ -d "${SPK_DIR}/conf" ]; then
    cp -r "${SPK_DIR}/conf" "${SPK_BUILD}/"
fi

# Copy WIZARD_UIFILES if any
if [ -d "${SPK_DIR}/WIZARD_UIFILES" ] && [ "$(ls -A ${SPK_DIR}/WIZARD_UIFILES 2>/dev/null)" ]; then
    cp -r "${SPK_DIR}/WIZARD_UIFILES" "${SPK_BUILD}/"
fi

# Move package.tgz to SPK build
mv "${BUILD_DIR}/package.tgz" "${SPK_BUILD}/"

echo "Creating SPK file..."
# Create the SPK file (which is just a tar archive)
SPK_FILE="${OUTPUT_DIR}/${PACKAGE_NAME}-${FULL_VERSION}.spk"
cd "${SPK_BUILD}"
tar cf "${SPK_FILE}" .
cd "${SCRIPT_DIR}"

# Cleanup build directory
rm -rf "${BUILD_DIR}"

echo ""
echo "==================================="
echo "Build complete!"
echo "==================================="
echo "SPK file: ${SPK_FILE}"
echo ""
echo "Installation instructions:"
echo "1. Open DSM Package Center"
echo "2. Click 'Manual Install'"
echo "3. Browse and select the SPK file"
echo "4. Follow the installation wizard"
echo ""
echo "After installation:"
echo "- Access Streamlit Hub at http://<your-nas-ip>:8501"
echo "- Add apps to /volume1/docker/streamlit-hub/apps/"
echo ""
