#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

# Function to set up the Python environment for each project
setup_python_environment() {
    local project_path="$1"
    local is_root="$2"

    echo "Configuring Python environment for project at $project_path..."

    # Convert project_path to an absolute path
    project_path=$(cd "$project_path" && pwd)

    # Check if a virtual environment already exists in .venv
    local venv_path="$project_path/.venv"
    if [ ! -d "$venv_path" ]; then
        echo "Creating a virtual environment at $venv_path..."
        python3 -m venv "$venv_path"
    else
        echo "Virtual environment already exists at $venv_path"
    fi

    # Activate the virtual environment
    # shellcheck disable=SC1091
    source "$venv_path/bin/activate"

    # Upgrade pip using python -m pip
    echo "Upgrading pip..."
    python -m pip install --upgrade pip

    # Initialize PYTHONPATH
    local pythonpath=""

    # Register editable packages
    if [ "$is_root" == "true" ]; then
        echo "Registering repo_packages in the root project..."
        pip install -e "$project_path/repo_packages"
        pythonpath="$project_path/repo_packages"
    else
        echo "Registering repo_packages and workspace_packages in subproject..."
        repo_path=$(cd "$project_path/../repo_packages" && pwd)
        workspace_path=$(cd "$project_path/workspace_packages" && pwd)
        pip install -e "$repo_path"
        pip install -e "$workspace_path"
        pythonpath="$repo_path:$workspace_path"
    fi

    # Create or overwrite the .env file with the absolute PYTHONPATH
    echo "Creating .env file with fully qualified PYTHONPATH..."
    echo "PYTHONPATH=$pythonpath" > "$project_path/.env"

    # Check if requirements.txt exists
    local requirements_path="$project_path/requirements.txt"
    if [ -f "$requirements_path" ]; then
        echo "Installing dependencies from $requirements_path..."
        pip install -r "$requirements_path"
    else
        echo "No requirements.txt found. Creating one..."
        pip freeze > "$requirements_path"
        echo "requirements.txt created at $requirements_path"
    fi

    # Deactivate the virtual environment
    echo "Deactivating virtual environment..."
    deactivate
}

# Main script execution

# Find the .code-workspace file
workspace_file=$(find . -maxdepth 1 -name "*.code-workspace" | head -n 1)

if [ -z "$workspace_file" ]; then
    echo "No *.code-workspace file found at the root of the repository."
    exit 1
fi

# Set up the root project first
setup_python_environment "." "true"

# Get the list of project folders
project_folders=$(jq -r '.folders[].path' "$workspace_file")

# Iterate over each project folder (excluding the root project) and set up the environment
for folder in $project_folders; do
    if [ "$folder" != "." ]; then
        setup_python_environment "$folder" "false"
    fi
done

echo "All projects have been configured successfully."
