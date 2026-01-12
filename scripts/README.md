# Scripts Directory

This directory contains utility scripts for managing the repository.

## Available Scripts

### import-from-recursive-eco.sh

**Purpose**: Automate importing files from the recursive-eco repository.

**Usage**:
```bash
# If recursive-eco is cloned in the parent directory
./scripts/import-from-recursive-eco.sh

# If recursive-eco is in a different location
./scripts/import-from-recursive-eco.sh /path/to/recursive-eco
```

**What it does**:
1. Verifies the source repository exists
2. Copies files from `apps/flow/public/data` to `data/`
3. Copies files from `apps/offer/public/templates` to `templates/`
4. Creates backups of placeholder files
5. Provides next-step instructions

**Prerequisites**:
- Access to the recursive-eco repository
- Bash shell
- File system permissions

## Adding New Scripts

When adding scripts to this directory:

1. Make them executable: `chmod +x script-name.sh`
2. Add clear comments explaining purpose
3. Include usage instructions at the top
4. Document the script in this README
5. Use consistent error handling
6. Provide helpful output messages

## Best Practices

- Test scripts thoroughly before committing
- Handle errors gracefully
- Provide clear user feedback
- Don't make destructive changes without confirmation
- Document any assumptions or requirements
