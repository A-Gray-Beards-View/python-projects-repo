# python-projects-repo

 This project has been created as a template to manage Python projects and sub-projects on multiple platforms using Visual Studio Code.

 There may be links to more detailed markdown files that are in the repository in this document.

## Project Charter

 1. This repository will be a template to be used to create new Python project repositories
 2. This repository has been designed to work with Visual Studio Code Workspaces
 3. The root of the repository is designed to provide common artifacts for sub-projects which is where unique work will be created. It will provide tools to support the management of those sub-projects
 4. The repository is intended to support multiple platforms so naming conventions were designed to be case-insensitive
 5. Best practices will be used, documented, and explained as a learning opportunity for all developers at any stage in their career
 6. The project has been designed to keep passwords and application keys locally so they are not checked into the GitHub repositories.
 7. All Python files can be run in the sub-folder they are located using "Play" button in the Visual Studio Code editor

## Documentation

### Naming Conventions

 Naming conventions in this project will follow standards used by most Python users. More specific conventions based on the author's decades of experience will be added and explained as required. With code, there are three important things to understand
 1. Purpose: What is the object capable of doing?
 2. Scope: What is the scope of the object? Global or local?
 3. Specifity: What is uniquely specific to this object? Is it a class with only static methods? A singleton? Is it fulfilling a specific architectural pattern?

#### Naming Convention Rules

* Class names will use CamelCase while class functions and properties will use snake_case
* Other than the default README.md which uses upper-case all file and folder names will be lower-case.
  * File and folder names will use snake_case all in lower-case, only the repository name and folder will use hyphens
  * All Python files that have a class will have the prefix 'cls_' but the CamelCase name of the class will be converted to snake_case for the file system. Example UsefulPythonObject class will become cls_useful_python_object.py
* JSON configuration files will have two conventions. Properties that map directly to a Python variable will use snake_case for the name. Properties that do not map directly to a Python variable will use JSON camelCase
* Classes that have all static methods will have a suffix like "Helper", or "Tools"
* Classes that are a singleton will have the suffix Singleton

## Using the Project

In order to run the code the virtual environments and specific configuration items need to be set. There are two scripts that will assist with that test. One is a shell script for MacOS, while the other is a Powershell script for Windows.

If you run into permission issues on MacOS or Linux, run the following command
> chmod -R u+rwx,g+rwx,o+rwx {Path to the repository}/python-projects-repo

[Project Layout](docs/README_project-layout.md)

### New Fork of the Repository

If you have created a new fork of this repository you need to do the following:
1. Open up a bash terminal at the root of the repository
2. Run ./shell_scripts/setup_root_project.sh

The script will determine the name of the repository and create a workspace file with the same name and prepare the root project as well as the two default sub-projects google-bigquery and google-cloud-storage

### Clone of Repository on a different system

I've created this project to be used on multiple operating systems. A requirement for a recent project I was working on. Secrets in the app_keys.json file and the key_files folder are not part of the repository by design for security purposes. They need to be manually copied to new computers.

Host specific config files in the format config.[HOST-NAME].json files can be checked in and stay in the repository if they do not contain secrets.

Once the clone is ready, you have to Run Task and select "Setup All Projects" which will run the bash script required on all Mac or LINUX operating systems or the Powershell script on Windows.

### Adding new sub-projects

There is a task added in tasks.json to add sub-projects. You simply Run Task 'Add Sub-Project' then it will prompt for the name of the sub-project which will create the folders, add it to the repository workspace, and initialize the virtual environment.

### Removing sub-projects

1. Delete the sub-project and all it's contents
2. Remove the sub-project entry from the "folders" section of the repository workspace JSON file