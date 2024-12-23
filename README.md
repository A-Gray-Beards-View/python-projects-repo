# python-projects-repo ALPHA

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

> NOTE: See the repository issues because this project is still in Alpha mode

## Naming Conventions

The naming conventions are intentional and described in the linked document. [Naming Convention Document](docs/README_naming-conventions.md)

## Design Elements

- The folder ```repo_packages``` is an editable package with code available to all projects including the sub-projects
- In sub-projects there is a ```workspace_packages``` folder with packages specific to that folder
- All of the scripts in the ```repo_packages``` have a ```main()``` method to test and demostrate the script
- The ```cls_env_config.py``` module has a singleton that should be in all scripts that require configuration settings. The configuration json files are combined using rules that can be understood by viewing that file.
- The ```cls_logging_manager.py``` has logging features that automatically log to file and the console using color
- Any script can be run hitting the play button in the script editor and it will run the script in the correct virtual environment based on the settings in the workspace and using the root project os sub-project ```.env``` files
- Because all shared packages scripts are marked as editable you can make changes to the files which will impact scripts using the modules immediately, except with Jupyter Notebooks which must reload the shared modules

## Project Configuration

In order to run the code the virtual environments and specific configuration items need to be set. There are two scripts that will assist with that test. One is a shell script for MacOS, while the other is a Powershell script for Windows.

If you run into permission issues on MacOS or Linux, run the following command
> chmod -R u+rwx,g+rwx,o+rwx {Path to the repository}/python-projects-repo

### Project Layout

The project layout is deliberated and intended to meet the project charter. [Project Layout Document](docs/README_project-layout.md)

### Scripts and Instructions

The following scripts are used to:
1. Setup a new fork
2. Clone the repository on a new computer
3. Add a new sub-project

#### New Fork of the Repository

If you have created a new fork of this repository you need to do the following:
1. Open up a bash terminal at the root of the repository
2. Run ./shell_scripts/setup_root_project.sh

The script will determine the name of the repository and create a workspace file with the same name and prepare the root project as well as the two default sub-projects google-bigquery and google-cloud-storage

#### Clone of Repository on a different system

I've created this project to be used on multiple operating systems. A requirement for a recent project I was working on. Secrets in the app_keys.json file and the key_files folder are not part of the repository by design for security purposes. They need to be manually copied to new computers.

Host specific config files in the format config.[HOST-NAME].json files can be checked in and stay in the repository if they do not contain secrets.

Once the clone is ready, you have to Run Task and select "Setup All Projects" which will run the bash script required on all Mac or LINUX operating systems or the Powershell script on Windows.

#### Adding new sub-projects

There is a task added in tasks.json to add sub-projects. You simply Run Task 'Add Sub-Project' then it will prompt for the name of the sub-project which will create the folders, add it to the repository workspace, and initialize the virtual environment.

### Removing sub-projects

1. Delete the sub-project and all it's contents
2. Remove the sub-project entry from the "folders" section of the repository workspace JSON file