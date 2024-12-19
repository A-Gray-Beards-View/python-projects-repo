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
