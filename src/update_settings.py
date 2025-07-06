import os
import json
import logging

from pathlib import Path
import re

# <TODO>
# - Add documentation
# - Add a check to see if the workspace file is already up to date
# - Add a check to see if the project settings are already up to date
# - Add a check to see if the workspace settings are already up to date
# - Add a check to see if the workspace file is already up to date
# - Add a check to see if the project settings are already up to date
# - Add a check to see if the workspace settings are already up to date
# </TODO>

def find_repo_root():
    """
    Finds the repository root.
    """
    current_path = Path.cwd()
    while current_path != current_path.parent:
        if (current_path / '.git').exists():
            return current_path
        current_path = current_path.parent
    return None

def find_workspace_file():
    """
    Finds the first `.code-workspace` file in the repository root.
    """
    repo_root = find_repo_root()
    if not repo_root:
        print("Repository root not found.")
        return None

    for file in os.listdir(repo_root):
        if file.endswith(".code-workspace"):
            return repo_root / file
    return None

def get_workspace_folders(workspace_file):
    """
    Extracts the project paths from the `folders` section of the workspace file.
    """
    with open(workspace_file, "r") as file:
        workspace = json.load(file)

    if "folders" not in workspace:
        print("No 'folders' section found in the workspace file.")
        return []

    return [folder["path"] for folder in workspace["folders"]]

def update_json_file(file_path, new_data):
    """
    Updates a JSON file only if the content needs to be changed.
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, "r") as file:
        current_data = json.load(file)

    if current_data == new_data:
        print(f"No changes needed for: {file_path}")
        return

    with open(file_path, "w") as file:
        json.dump(new_data, file, indent=4)
        print(f"Updated file: {file_path}")

def update_workspace_file(workspace_file, repo_name):
    """
    Updates the `.code-workspace` file with workspace-wide settings.
    """
    print(f"Checking workspace file: {workspace_file}")

    try:
        with open(workspace_file, "r") as file:
            workspace = json.load(file)

        if "settings" not in workspace:
            workspace["settings"] = {}

        new_settings = {
            "terminal.integrated.env.linux": {
                "REPO_ROOT": "${workspaceFolder:" + repo_name + "}",
                "WORKSPACE_ROOT": "${workspaceFolder}",
                "PYTHONPATH": "${workspaceFolder:" + repo_name + "}/repo_packages;${workspaceFolder}/workspace_packages"
            },
            "terminal.integrated.env.windows": {
                "REPO_ROOT": "${workspaceFolder:" + repo_name + "}",
                "WORKSPACE_ROOT": "${workspaceFolder}",
                "PYTHONPATH": "${workspaceFolder:" + repo_name + "}/repo_packages;${workspaceFolder}/workspace_packages"
            },
            "terminal.integrated.env.osx": {
                "REPO_ROOT": "${workspaceFolder:" + repo_name + "}",
                "WORKSPACE_ROOT": "${workspaceFolder}",
                "PYTHONPATH": "${workspaceFolder:" + repo_name + "}/repo_packages;${workspaceFolder}/workspace_packages"
            },
            "powershell.cwd": repo_name,
            "search.exclude": {
                "**/.venv/": True,
                "**/samples/": True,
                "**/tmp/": True
            }
        }

        if workspace["settings"] != new_settings:
            workspace["settings"] = new_settings
            with open(workspace_file, "w") as file:
                json.dump(workspace, file, indent=4)
                print(f"Updated workspace file: {workspace_file}")
        else:
            print(f"No changes needed for workspace file: {workspace_file}")

    except Exception as e:
        print(f"Error updating workspace file: {e}")

def update_project_settings(project_paths, repo_root, repo_name):
    """
    Updates `.vscode/settings.json` files for each project path in the workspace.
    """    
    for project_path in project_paths:
        # Convert project path to absolute path
        abs_project_path = Path(repo_root) / project_path
        settings_path = abs_project_path / ".vscode/settings.json"
        
        if not settings_path.exists():
            print(f"Settings file not found for project: {settings_path}")
            continue

        # Get project name from path for workspace variable
        project_name = project_path.upper() if project_path != "." else repo_name
        is_repo_root = project_path == "."

        if os.name == "nt":  # Windows
            interpreter_path = "${workspaceFolder:" + project_name + "}\\.venv\\Scripts\\python.exe"
            env_path = "${workspaceFolder:" + project_name + "}/.env"
        else:
            interpreter_path = "${workspaceFolder:" + project_name + "}/.venv/bin/python"
            env_path = "${workspaceFolder:" + project_name + "}/.env"

        with open(settings_path, "r") as file:
            settings = json.load(file)

        # Set extra paths based on whether this is repo root or subproject
        extra_paths = ["${workspaceFolder:" + repo_name + "}/repo_packages"]
        if not is_repo_root:
            extra_paths.append("${workspaceFolder:" + project_name + "}/workspace_packages")

        new_settings = settings.copy()
        new_settings.update({
            "python.defaultInterpreterPath": interpreter_path,
            "python.envFile": env_path,
            "python.analysis.extraPaths": extra_paths,
            "python.analysis.autoImportCompletions": True,
            "python.terminal.activateEnvironment": True,
            "python.terminal.activateEnvInCurrentTerminal": True,
            "python.terminal.executeInFileDir": True,
            "python.terminal.focusAfterLaunch": True,
            "python.terminal.launchArgs": []
        })

        if settings != new_settings:
            with open(settings_path, "w") as file:
                json.dump(new_settings, file, indent=4)
                print(f"Updated settings for project: {settings_path}")
        else:
            print(f"No changes needed for project settings: {settings_path}")

            # Temporarily disable terminal settings for Windows PowerShell
            #"terminal.integrated.profiles.windows": {
            #    "Windows PowerShell": {
            #        "path": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
            #        "args": [
            #            "-NoExit",
            #            "-Command",
            #            f"& {{ . \"${{workspaceFolder}}/.venv/Scripts/Activate.ps1\" }}"
            #        ]
            #    }
            #}

def main():
    """
    Main function to update all configuration files.
    """
    # Find the repository root first
    repo_root = find_repo_root()
    if not repo_root:
        print("Repository root not found.")
        return

    # Calculate repo_name once
    repo_name = repo_root.name.upper()

    # Store current working directory
    original_cwd = Path.cwd()
    try:
        # Change to repo root for workspace operations
        os.chdir(repo_root)

        # Find the workspace file
        workspace_file = find_workspace_file()
        if workspace_file:
            print(f"Workspace file found: {workspace_file}")
            # Update workspace settings
            update_workspace_file(workspace_file, repo_name)

            # Get project paths from the workspace file
            project_paths = get_workspace_folders(workspace_file)

            # Update project settings with repo root
            update_project_settings(project_paths, repo_root, repo_name)
        else:
            print("No workspace file found.")

    finally:
        # Restore original working directory
        os.chdir(original_cwd)


if __name__ == "__main__":
    main()
