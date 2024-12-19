#!/bin/bash

# Determine the directory of the current script
script_dir="$(dirname "${BASH_SOURCE[0]}")"

repo_root=""
repo_name=""

# Check if the script is already sourced
if [ -z "${SCRIPT_INCLUDED+x}" ]; then
    # shellcheck disable=SC1091
    source "$script_dir/common.sh"
    SCRIPT_INCLUDED=1
fi

# Create the root project workspace if it doesn't exist
create_root_project_workspace() {
    local repo_root="$1"
    local repo_name="$2"

    echo "Creating root project workspace..."
    copy_template_if_not_exists "$repo_root/templates/[REPO-NAME].code-workspace" "$repo_root/$repo_name.code-workspace"

    echo "Find and replace [REPO-NAME] with the actual repository name"
    find_and_replace "\[REPO-NAME\]" "$repo_name" "$repo_root/$repo_name.code-workspace"

    echo "Copy the launch.json file to the .vscode folder"
    copy_template_if_not_exists "$repo_root/templates/launch.json" "$repo_root/.vscode/launch.json"

    echo "Find and replace [REPO-NAME] with the actual repository name"
    find_and_replace "\[REPO-NAME\]" "$repo_name" "$repo_root/.vscode/launch.json"
}

create_root_project_workspace "$repo_root" "$repo_name"

create_venv "$repo_root/.venv"

# Install the default packages
pip install -r "$repo_root/requirements.txt"
