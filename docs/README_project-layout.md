# Project Layout

This Github repository has been setup with a Visual Studio Code workspace with a root project at the root of the repository that has sub-projects. The root project has a shared library that can be used by all sub-projects. This document is how to create a new sub-project.

## Repository Layout

### Root Repository Starting Layout

root_folder/
├── .vscode/                          # Settings files for Visual Studio Code
│   ├── launch.json
│   ├── settings.json
│   └── tasks.json
├── .gitattributes
├── .gitignore
├── key_files/                        # Folder to hold application key files that are NOT checked into GitHub
├── repo_packages/                    # Shared packages for the entire repository
├── sql_scripts/                      # SQL scripts global to the entire repository
├── tests/                            # Test scripts for the entire repository
├── templates/
│   ├── template.app_keys.json        # Template for creating the app_keys.json file
│   ├── template.code-workspace       # Template for creating the repository workspace file
│   └── template.config.hostname.json # Template for creating the config.hostname.json file for each system using the repository
├── tools/                            # Tools to be used by the entire repository
├── config.json                       # Configuration settings for the entire repository
├── LICENSE                           # License file for the repository
├── README.md
├── requirements.txt                  # Baseline Python dependencies for the root project
├── setup_python_projects.sh          # Bash script to setup the workspace(s)
├── Setup-Python-Projects.ps1         # Powershell Script to setup the workspace(s)
└── template.code-workspace           # Visual Studio Code workspace file to be named to match the repository

### Files and folders added to the root repository after initialization

root_folder/
├── .venv/                            # Local Python environment for the root of the repository
├── .vscode/
├── .env # An environment file that has to be added manually (might add it to Git)
├── config.[hostname].json            # The [hostname] should match the name of the computer
├── app_keys.json                     # A keys file that must be manually added and cannot be in Git
└── [repository].code-workspace       # The [respository] variable should match the repository name

### A fully working repository with the minimum files for a sub-project

root_folder/
├── 
├── sub-project1/
│   ├── .vscode/
│   └── 
│   
└── 

To setup the new sub-project you simply create those files. The requirements.txt could be empty if there is no scripts yet in the shared folder. Then add a sub-project line in the setup_workspace scripts which is documented in them and run it! That will then prepare the sub-project for use. The .vscode can be a copy of the settings files in the root repository. Supposedly the settings are inherited but I've not experienced that.

Alt+179 │
Alt+195 ├
Alt+192 └
Alt+196 ─