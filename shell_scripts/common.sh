#!/bin/bash

# Get the absolute path of the root of the Git repository
repo_root=$(git rev-parse --show-toplevel)

# Extract the folder name from the path
repo_name=$(basename "$repo_root")

# Print the name of the folder
echo "The root folder of the repository is: $repo_name"

copy_template_if_not_exists() {
    local template_path=$1
    local target_path=$2

    if [ ! -f "$target_path" ]; then
        cp "$template_path" "$target_path"
    else
        echo "File '$target_path' already exists."
    fi
}

# Function to find and replace a string in a file
find_and_replace() {
    local search_string=$1
    local replace_string=$2
    local file_path=$3

    sed -i '' "s/$search_string/$replace_string/g" "$file_path"
}

# Function to create a virtual environment
create_venv() {
    local venv_path=$1

    # Check if the virtual environment already exists
    if [ -d "$venv_path" ]; then
        echo "Virtual environment already exists at $venv_path"
        return
    fi

    # Create a new virtual environment
    echo "Creating a new virtual environment at $venv_path"
    python3 -m venv "$venv_path"
}

# Function to set up the Python environment for each project
setup_python_environment() {
    local project_path="$1"
    local is_root="$2"

    echo "Configuring Python environment for project at $project_path..."

    # Convert project_path to an absolute path
    project_path=$(cd "$project_path" && pwd)

    # Check if a virtual environment already exists in .venv
    local venv_path="$project_path/.venv"

    create_venv "$venv_path"

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

