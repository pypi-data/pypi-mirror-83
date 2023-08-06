# Create PyProj

```text
   ______                __          ____        ____               _
  / ____/_______  ____ _/ /____     / __ \__  __/ __ \_________    (_)
 / /   / ___/ _ \/ __ `/ __/ _ \   / /_/ / / / / /_/ / ___/ __ \  / /
/ /___/ /  /  __/ /_/ / /_/  __/  / ____/ /_/ / ____/ /  / /_/ / / /
\____/_/   \___/\__,_/\__/\___/  /_/    \__, /_/   /_/   \____/_/ /
                                       /____/                /___/
```

## Create a new python skeleton project.

usage:

```python
create-pyproj <projectname>
```

The project structure will be copied to the folder ./\<projectname\>, the modules installed with Pipenv and a git repo initiated.

--------------------------------

The project has a number of development tools
and convenince functions to get you started quickly!

This basic version starts with:

- settings manager, save, load and update using yaml.
- a logging setup with console and file handlers.
- a version manager, to keep the version file easily asccessible for CI/CD

## Project structure

```text
    - .vscode
        - settings.json
    - src
        - _config
            - logging.py
            - logging.yaml
            - settings.py
            - version.py
        - main.py
        - settings.yaml
    - .env
    - .flake8
    - .style.yapf
    - .gitignore
    - Pipfile
    - README.md
    - VERSION
```
