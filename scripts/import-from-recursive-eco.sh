#!/usr/bin/env bash
# Import script for bringing in files from recursive-eco repository
# This script should be run by someone with access to the source repository

set -e

# Configuration
SOURCE_REPO_PATH="${1:-../recursive-eco}"
TARGET_REPO_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "=== recursive.eco-schemas Import Script ==="
echo "Source: $SOURCE_REPO_PATH"
echo "Target: $TARGET_REPO_PATH"
echo ""

# Check if source repository exists
if [ ! -d "$SOURCE_REPO_PATH" ]; then
    echo "ERROR: Source repository not found at: $SOURCE_REPO_PATH"
    echo ""
    echo "Please either:"
    echo "  1. Clone the repository: git clone https://github.com/PlayfulProcess/recursive-eco.git"
    echo "  2. Provide the path as an argument: ./import-from-recursive-eco.sh /path/to/recursive-eco"
    exit 1
fi

# Check for flow data directory
FLOW_DATA_SOURCE="$SOURCE_REPO_PATH/apps/flow/public/data"
if [ -d "$FLOW_DATA_SOURCE" ]; then
    echo "✓ Found flow data directory"
    
    # Count files
    FILE_COUNT=$(find "$FLOW_DATA_SOURCE" -type f | wc -l)
    echo "  Files to import: $FILE_COUNT"
    
    # Create backup of placeholder
    if [ -f "$TARGET_REPO_PATH/data/.import-placeholder.json" ]; then
        mv "$TARGET_REPO_PATH/data/.import-placeholder.json" "$TARGET_REPO_PATH/data/.import-placeholder.json.backup"
    fi
    
    # Copy files
    echo "  Copying flow data files..."
    if [ -n "$(ls -A "$FLOW_DATA_SOURCE" 2>/dev/null)" ]; then
        cp -rv "$FLOW_DATA_SOURCE"/* "$TARGET_REPO_PATH/data/"
    else
        echo "  (no files to copy - source directory is empty)"
    fi
    
    echo "  ✓ Flow data imported"
else
    echo "⚠ Flow data directory not found: $FLOW_DATA_SOURCE"
fi

echo ""

# Check for offer templates directory
OFFER_TEMPLATES_SOURCE="$SOURCE_REPO_PATH/apps/offer/public/templates"
if [ -d "$OFFER_TEMPLATES_SOURCE" ]; then
    echo "✓ Found offer templates directory"
    
    # Count files
    FILE_COUNT=$(find "$OFFER_TEMPLATES_SOURCE" -type f | wc -l)
    echo "  Files to import: $FILE_COUNT"
    
    # Create backup of placeholder
    if [ -f "$TARGET_REPO_PATH/templates/.import-placeholder.json" ]; then
        mv "$TARGET_REPO_PATH/templates/.import-placeholder.json" "$TARGET_REPO_PATH/templates/.import-placeholder.json.backup"
    fi
    
    # Copy files
    echo "  Copying offer template files..."
    if [ -n "$(ls -A "$OFFER_TEMPLATES_SOURCE" 2>/dev/null)" ]; then
        cp -rv "$OFFER_TEMPLATES_SOURCE"/* "$TARGET_REPO_PATH/templates/"
    else
        echo "  (no files to copy - source directory is empty)"
    fi
    
    echo "  ✓ Offer templates imported"
else
    echo "⚠ Offer templates directory not found: $OFFER_TEMPLATES_SOURCE"
fi

echo ""
echo "=== Import Complete ==="
echo ""
echo "Next steps:"
echo "  1. Review imported files: cd $TARGET_REPO_PATH"
echo "  2. Check for sensitive information and anonymize if needed"
echo "  3. Add documentation for imported files"
echo "  4. Update README files in data/ and templates/ directories"
echo "  5. Commit changes: git add . && git commit -m 'Import files from recursive-eco'"
echo ""
echo "Note: Please review all imported files before committing!"
