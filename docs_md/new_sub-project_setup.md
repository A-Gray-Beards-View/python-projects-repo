# Process to Create a New Sub-Project

This Github repository has been setup with a Visual Studio Code workspace with a root project at the root of the repository that has sub-projects. The root project has a shared library that can be used by all sub-projects. This document is how to create a new sub-project.

## Repository Layout

Root Repository Starting Layout
root_folder/
├── .vscode/                          # Settings files for Visual Studio Code
├── shared/                           # Shared packages for the entire repository
├── .gitattributes
├── .gitignore
├── config.json                       # Configuration settings for the entire repository
├── readme.md
├── requirements.txt                  # The baseline dependencies for a new project
├── setup_workspace.ps1               # Powershell Script to setup the workspace(s)
├── setup_workspace.sh                # Bash script to setup the workspace(s)
└── {Repository Name}.code-workspace  # Visual Studio Code workspace file to be named to match the repository

A fully working repository with no sub-projects or script sub-folders
root_folder/
├── .venv/ # Local python environment added by the setup_workspace scripts
├── .vscode/
├── shared/
├── .env # An environment file that has to be added manually (might add it to Git)
├── .gitattributes
├── .gitignore
├── config.json
├── keys.json # A keys file that must be manually added and cannot be in Git
├── readme.md
├── requirements.txt
├── setup_workspace.ps1
├── setup_workspace.sh
└── uspto-patents-processing-python.code-workspace

A fully working repository with the minimum files for a sub-project
root_folder/
├── .venv/
├── .vscode/
├── sub-project1/
│   ├── .vscode/
│   ├── shared/
│   ├── readme.md
│   ├── requirements.txt
│   ├── setup.cfg
│   └── setup.py
│   
├── shared/
├── .env
├── .gitattributes
├── .gitignore
├── config.json
├── keys.json
├── readme.md
├── requirements.txt
├── setup_workspace.ps1
├── setup_workspace.sh
└── uspto-patents-processing-python.code-workspace

To setup the new sub-project you simply create those files. The requirements.txt could be empty if there is no scripts yet in the shared folder. Then add a sub-project line in the setup_workspace scripts which is documented in them and run it! That will then prepare the sub-project for use. The .vscode can be a copy of the settings files in the root repository. Supposedly the settings are inherited but I've not experienced that.

Alt+179 │
Alt+195 ├
Alt+192 └
Alt+196 ─