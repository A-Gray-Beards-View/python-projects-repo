# Project Layout

This Github repository has been setup with a Visual Studio Code workspace with a root project at the root of the repository that has sub-projects. The root project has a shared library that can be used by all sub-projects. This document is how to create a new sub-project.

## Repository Layout

### Root Repository New Fork Layout

```
root_folder/
│
├── .vscode/                          # Settings files for Visual Studio Code
│   ├── settings.json
│   └── tasks.json
│
├── .gitattributes
├── .gitignore
│
├── docs/                             # Additional documents about the project
│   └── README_project-layout.md     # This file
│
├── key_files/                        # Folder to hold application key files that are NOT checked into GitHub
│
├── repo_packages/
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
├── shell_scripts/                    # Shell scripts to manage the repository
│   ├── add_subproject.sh
│   ├── common.sh
│   ├── setup_python_projects.sh
│   ├── setup_root_project.sh
│   └── Setup-Python-Projects.ps1
│
├── templates/
│   ├── [REPO-NAME].code-workspace
│   ├── config.[HOST-MAC].json
│   ├── config.[HOST-PC].json
│   ├── launch.json
│   ├── settings.json
│   ├── setup.cfg
│   ├── setup.py
│   ├── tasks.json
│   ├── template.app_keys.json
│   └── template.config.[HOST].json
│
├── config.json                       # Configuration settings for the entire repository
├── LICENSE                           # License file for the repository
├── README.md
├── requirements.txt                  # Baseline Python dependencies for the root project
│
├── GOOGLE-BIGQUERY
└── GOOGLE-CLOUD-STORAGE
```

### Files and folders added to the root repository after initialization

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

Alt+179 │
Alt+195 ├
Alt+192 └
Alt+196 ─