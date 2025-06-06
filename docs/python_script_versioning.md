
# Python Script Versioning with Git Integration

This document outlines how to independently version multiple Python scripts in a single Git repository, using a `major.minor.release.build` format.

## Goals

- Each script tracks its own version.
- `major.minor.release` is manually defined inside the script.
- `build` is automatically updated based on commit history.
- Build number is updated only when the script is pushed.
- Prevents unnecessary updates to unrelated scripts.

---

## Version Pattern

```python
MAJOR = 1
MINOR = 2
RELEASE = 3

def get_build_number():
    import subprocess
    try:
        # Count commits affecting this script
        build = subprocess.check_output(["git", "rev-list", "--count", "HEAD", "--", __file__])
        return int(build.strip().decode("utf-8"))
    except Exception:
        return 0

BUILD = get_build_number()
__version__ = f"{MAJOR}.{MINOR}.{RELEASE}.{BUILD}"

if __name__ == "__main__":
    print(f"Script version: {__version__}")
```

---

## Optional: Automating the Build Number on Push

Create a Git **pre-push hook** (`.git/hooks/pre-push`) to automatically update the version:

```bash
#!/bin/bash

SCRIPT_TO_VERSION="my_script.py"

if git diff --name-only HEAD~1 HEAD | grep -q "$SCRIPT_TO_VERSION"; then
    VERSION=$(awk -F'= ' '/MAJOR/{maj=$2} /MINOR/{min=$2} /RELEASE/{rel=$2} END{print maj"."min"."rel}' "$SCRIPT_TO_VERSION")
    BUILD=$(git rev-list --count HEAD -- "$SCRIPT_TO_VERSION")
    sed -i "s/__version__ = .*/__version__ = \"$VERSION.$BUILD\"/" "$SCRIPT_TO_VERSION"
    git add "$SCRIPT_TO_VERSION"
    git commit -m "Updated build number for $SCRIPT_TO_VERSION to $BUILD"
fi
```

> Make sure the script is executable:
```bash
chmod +x .git/hooks/pre-push
```

---

## Optional: External Version File (`version.json`)

Instead of modifying the script, you can store version info in a JSON file.

**version.json**
```json
{
  "major": 1,
  "minor": 2,
  "release": 3,
  "build": 45
}
```

**Python Integration**
```python
import json

with open("version.json") as f:
    version_data = json.load(f)

__version__ = f"{version_data['major']}.{version_data['minor']}.{version_data['release']}.{version_data['build']}"
```

---

## Notes

- Git hooks must have **no file extension** (`pre-push`, not `pre-push.sh`).
- Always use UTC timestamps in versioning if recording time-based metadata.
- Tags and commit counts can also be used if a more centralized release process is desired.

---
