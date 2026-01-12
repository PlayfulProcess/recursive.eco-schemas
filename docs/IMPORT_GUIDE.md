# Importing Files from recursive-eco Repository

## Files to Import

### From `apps/flow/public/data`
These files contain data that circulates throughout the recursive.eco ecosystem (exportable/importable via offer tab or flow app) and should be organized into `/data/`:
- Review each file for its content type
- Understand these files are shared across the ecosystem, not just the flow app
- Anonymize any personal information
- Add context documentation explaining the data format
- Organize by date, reading type, or system used

### From `apps/offer/public/templates`  
These files contain offer templates that should be organized into `/templates/`:
- Review each template for reusability
- Add clear usage instructions
- Document required vs. optional parameters
- Ensure templates are generalizable

## Import Process

### Step 1: Access the Files
Since the source repository may be private, you can:
1. Clone the repository if you have access:
   ```bash
   git clone https://github.com/PlayfulProcess/recursive-eco.git
   ```
2. Or download specific files via the GitHub web interface
3. Or have someone with access export the files

### Step 2: Review and Prepare
For each file:
1. Understand its purpose and content
2. Check for personal or sensitive information
3. Determine the best location in this repository
4. Add appropriate documentation

### Step 3: Organize
Place files in appropriate directories:
- Flow data → `/data/`
- Offer templates → `/templates/`
- Schema definitions → `/schemas/` (in appropriate subdirectory)

### Step 4: Document
For each imported file or set of files:
1. Add a README explaining the source and purpose
2. Include any necessary context about format or usage
3. Credit the original source
4. Note any modifications made during import

## Automation Script

When ready to import, you can use this script structure:

```bash
#!/bin/bash
# import-files.sh

SOURCE_REPO="/path/to/recursive-eco"
TARGET_REPO="/home/runner/work/recursive.eco-schemas/recursive.eco-schemas"

# Import flow data
echo "Importing flow data..."
cp -r "$SOURCE_REPO/apps/flow/public/data"/* "$TARGET_REPO/data/"

# Import offer templates  
echo "Importing offer templates..."
cp -r "$SOURCE_REPO/apps/offer/public/templates"/* "$TARGET_REPO/templates/"

echo "Import complete! Please review and document the imported files."
```

## Next Steps After Import

1. Review all imported files
2. Add appropriate README files
3. Remove any sensitive information
4. Organize files logically
5. Update main documentation
6. Commit changes with descriptive messages
7. Invite community review

## Manual Import Guide

If you need to manually import specific files:

1. Identify the file in the source repo
2. Copy its contents
3. Create the file in the appropriate location here
4. Add source attribution in a comment or README
5. Document its purpose and usage

## Questions?

If you encounter issues during import:
- Check file formats and compatibility
- Verify no sensitive data is included
- Ensure proper attribution
- Ask the community for guidance via issues
