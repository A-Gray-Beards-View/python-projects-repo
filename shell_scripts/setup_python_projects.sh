#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

# Determine the directory of the current script
script_dir="$(dirname "${BASH_SOURCE[0]}")"

#repo_root=""
#repo_name=""

# Check if the script is already sourced
if [ -z "${SCRIPT_INCLUDED+x}" ]; then
    # shellcheck disable=SC1091
    source "$script_dir/shell_scripts/common.sh"
    SCRIPT_INCLUDED=1
fi

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
