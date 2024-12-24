# Project Layout

This Github repository has been setup with a Visual Studio Code workspace with a root project at the root of the repository that has sub-projects. The root project has a shared library that can be used by all sub-projects. This document is how to create a new sub-project.

## Repository Layout

### Root Repository New Fork Layout

```
root_folder/
│
├── .vscode/                          # Settings files for Visual Studio Code
│   ├── python.json.code-snippets     # Demonstration of Python code snippers with one entry
│   ├── settings.json                 # Default settings.json used by the root, not the sub-projects
│   └── tasks.json                    # Default tasks.json used by the root, not the sub-projects
│
├── .gitattributes
├── .gitignore
│
├── docs_md/                          # Additional documents about the project linked from the ./README.md file
│   ├── README_naming-conventions.md  # Naming conventions used in the project
│   └── README_project-layout.md      # This file
│
├── key_files/                        # Folder to hold application key files that are NOT checked into GitHub
│
├── repo_packages/                    # Editable package to hold modules used by the root project and sub-projects
│   ├── __init__.py
│   ├── cls_env_config.py
│   ├── cls_env_tools.py
│   ├── cls_logging_manager.py
│   ├── cls_string_helpers.py
│   ├── cls_xml_helpers.py
│   ├── postgres_helpers.py
│   ├── setup.cfg
│   └── setup.py
│
├── scripts_powershell/               # Powershell scripts to manage the repository
│   ├──
│   ├──
│   ├──
│   ├──
│   └── Setup-Python-Projects.ps1
│
├── scripts_shell/                    # Shell scripts to manage the repository
│   ├── add_subproject.sh             # Script to create sub-projects triggered by 'Run Tasks' as a command
│   ├── common.sh                     # Used by other scripts in this folder
│   ├── setup_python_projects.sh      # Triggered by Run Task to initialize the root and sub-projects after cloning the repository
│   └── setup_root_project.sh         # Run on the command line after forking the repository
│
├── templates/
│   ├── [REPO-NAME].code-workspace    # Template code-workspace used by Setup Root Project script
│   ├── config.[HOST-MAC].json        # Template script to be used manually
│   ├── config.[HOST-PC].json         # Template script to be used manually
│   ├── launch.json                   # Template script copied/modified by Setup Root Project script
│   ├── settings.json                 # Template script copied/modified for Add Sub-Project script
│   ├── setup.cfg
│   ├── setup.py
│   ├── tasks.json                    # Template script copied/modified for Add Sub-Project script
│   ├── template.app_keys.json        # Example app_keys.json file
│   └── template.config.[HOST].json   # Example config.HOST.json file
│
├── config.json                       # Configuration settings for the entire repository
├── LICENSE                           # License file for the repository
├── README.md
├── requirements.txt                  # Baseline Python dependencies for the root project
│
├── GOOGLE-BIGQUERY                   # Example project for using Google BigQuery
└── GOOGLE-CLOUD-STORAGE              # Example project for using Google Cloud Storage
```

### Files and folders added to the root repository after set up script initialization

```
root_folder/
├── .venv/                            # Local Python environment for the root of the repository
├── .vscode/launch.json
├── .env # An environment file that has to be added manually (might add it to Git)
└── [REPO-NAME].code-workspace        # The [respository] variable should match the repository name
 ```

### A fully working repository with the minimum files for a sub-project

```
repository_root_folder/
└── sub_project_root/
    ├── .venv/
    ├── .vscode/
    │   ├── launch.json
    │   ├── settings.json
    │   └── tasks.json
    │
    ├── workspace_packages
    │   ├── __init__.py
    │   ├── setup.cfg
    │   └── setup.py
    │
    ├── .env
    └── requirements.txt
```

#### Symbols for copy/pasting

```
Alt+179 │
Alt+195 ├
Alt+192 └
Alt+196 ─
```