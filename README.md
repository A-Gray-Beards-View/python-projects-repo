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