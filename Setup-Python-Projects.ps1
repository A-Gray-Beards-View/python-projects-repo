# Exit immediately if a command exits with a non-zero status
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# Function to set up the Python environment for each project
function Initialize-PythonEnvironment {
    param (
        [string]$projectPath,
        [bool]$isRoot
    )

    Write-Host "Configuring Python environment for project at $projectPath..."

    # Convert project_path to an absolute path
    $projectPath = Resolve-Path -Path $projectPath

    # Check if a virtual environment already exists in .venv
    $venvPath = Join-Path $projectPath ".venv"
    if (-Not (Test-Path -Path $venvPath)) {
        Write-Host "Creating a virtual environment at $venvPath..."
        python -m venv $venvPath
    } else {
        Write-Host "Virtual environment already exists at $venvPath"
    }

    # Activate the virtual environment
    $venvActivate = Join-Path $venvPath "Scripts\Activate.ps1"
    & $venvActivate

    # Upgrade pip
    Write-Host "Upgrading pip..."
    python -m pip install --upgrade pip

    # Initialize PYTHONPATH
    $pythonpath = ""

    # Register editable packages
    if ($isRoot) {
        Write-Host "Registering repo_packages in the root project..."
        pip install -e "$projectPath\repo_packages"
        $pythonpath = "$projectPath\repo_packages"
    } else {
        Write-Host "Registering repo_packages and workspace_packages in subproject..."
        $repoPath = Resolve-Path -Path "$projectPath\..\repo_packages"
        $workspacePath = Resolve-Path -Path "$projectPath\workspace_packages"
        pip install -e $repoPath
        pip install -e $workspacePath
        $pythonpath = "$repoPath;$workspacePath"
    }

    # Create or overwrite the .env file with the absolute PYTHONPATH
    Write-Host "Creating .env file with fully qualified PYTHONPATH..."
    Set-Content -Path "$projectPath\.env" -Value "PYTHONPATH=$pythonpath"

    # Check if requirements.txt exists
    $requirementsPath = Join-Path $projectPath "requirements.txt"
    if (Test-Path -Path $requirementsPath) {
        Write-Host "Installing dependencies from $requirementsPath..."
        pip install -r $requirementsPath
    } else {
        Write-Host "No requirements.txt found. Creating one..."
        pip freeze | Out-File -FilePath $requirementsPath
        Write-Host "requirements.txt created at $requirementsPath"
    }

    # Deactivate the virtual environment
    Write-Host "Deactivating virtual environment..."
    deactivate
}

# Main script execution

# Find the .code-workspace file
$workspaceFile = Get-ChildItem -Filter "*.code-workspace" | Select-Object -First 1

if (-Not $workspaceFile) {
    Write-Host "No *.code-workspace file found at the root of the repository."
    exit 1
}

# Set up the root project first
Setup-PythonEnvironment -projectPath "." -isRoot $true

# Get the list of project folders
$projectFolders = (Get-Content $workspaceFile.FullName | ConvertFrom-Json).folders.path

# Iterate over each project folder (excluding the root project) and set up the environment
foreach ($folder in $projectFolders) {
    if ($folder -ne ".") {
        Initialize-PythonEnvironment -projectPath $folder -isRoot $false
    }
}

Write-Host "All projects have been configured successfully."
