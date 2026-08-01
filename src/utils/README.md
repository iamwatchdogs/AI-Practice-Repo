# Utility Package

The utility packages consists of modules, script and programs required across repo for various activities. This repo consists of following utilities;

- [Create New Project](#create-new-project)

## Create New Project

**Create New Project** utility is a common utility that helps me initialize a few project within the `src` directory with ease.

These are the following steps performed by this script,

- [x] Create a new package within `src` directory.
- [x] Add templated `.env.example` file with details into newly created package.
- [x] Add templated `__init__.py` file with details into newly created package.
- [x] Add templated `main.py` file with details into newly created package.
- [x] Add templated `README.md` file with details into newly created package.
- [x] Register the new package within `pyproject.toml`. That includes,
  - [x] Added the new package to hatch wheels.
  - [x] Creating script.
  - [x] Adding package to mypy package list.
- [x] Register the new package within `_config.yaml` for GitHub Pages.
- [x] Update the index on `README.md` file at the root of the repo.

The `create_new_project.py` script can be use either directly using command line args or via interactive session and this script takes the following inputs:

| Inputs               | Type     | Description                                                   |
| :------------------: | :------: | :-----------------------------------------------------------: |
| Project Number       | Required | Sequence of the project                                       |
| Project Name         | Required | Name of the project                                           |
| Package Name         | Required | Package Alias to create full package name                     |
| UI Subtitle          | Required | A oneline description to be displayed on GitHub Pages         |
| Project Description  | Optional | Sets the project description on `__init__.py` and `README.md` |
| Project Dependencies | Optional | Sets the required dependencies on `README.md`                 |

> [!NOTE]
>
> The full package name is derived by combining **Project Number** and **Package Name** i.e., `proj_{PROJECT_NUMBER}_{PACKAGE_NAME}`.

### Command-Line Mode

Here's a quick usage of the cmd args usage:

```bash
uv run create_new_project \
  --number 10 \
  --package intro_to_rag \
  --title "Intro to RAG" \
  --ui-subtitle "A retrieval-augmented generation project"
```

> [!NOTE]
> If you didn't mentioned any optional fields, then it will keep the place holder present within the template as-is.

<details>
<summary>
All cmd args usage details
</summary>

All details can be found by using `--help` flag. Here's the all the details:

```bash
$ uv run create_new_project --help
usage: create_new_project [-h] --number NUMBER --package PACKAGE --title TITLE --ui-subtitle UI_SUBTITLE [--description DESCRIPTION] [--deps [DEPS ...]] [--force] [--silent]
                          [--dry-run]

Create a practice project from src/utils/templates.

options:
  -h, --help            show this help message and exit
  --number NUMBER       Required positive project number, for example 2.
  --package PACKAGE     Required lowercase package component, for example intro_to_rag.
  --title TITLE         Required human-readable project title.
  --ui-subtitle UI_SUBTITLE
                        Required subtitle written to the GitHub Pages configuration.
  --description DESCRIPTION
                        Optional value for the [PROJECT_DESCRIPTION] template marker.
  --deps [DEPS ...]     Optional dependencies used to replace dependency template markers.
  --force               Overwrite the destination package if it already exists.
  --silent              Suppress normal progress logs; errors are still shown.
  --dry-run             Show planned actions without creating or modifying files.

Interactive mode:
  Run without arguments to enter the required values interactively. The script
  then prompts for each optional square-bracket template marker. Press Enter
  without a value to keep that marker unchanged.

Command-line examples:
  uv run create_new_project
  uv run create_new_project \
    --number 2 \
    --package intro_to_rag \
    --title "Intro to RAG" \
    --ui-subtitle "A retrieval-augmented generation project"
  uv run create_new_project \
    --number 2 \
    --package intro_to_rag \
    --title "Intro to RAG" \
    --ui-subtitle "A retrieval-augmented generation project" \
    --description "Practice retrieval-augmented generation" \
    --deps openai pydantic

The generated package is written to:
  src/proj_{PROJECT_NUMBER}_{PROJECT_PACKAGE}

The command also updates pyproject.toml, _config.yaml, and the root README.md
unless --dry-run is supplied. Use --silent to suppress progress logs.
```

</details>

### Interactive Mode

Run without arguments to be prompted for the four required values and all optional square-bracket markers:

```bash
uv run create_new_project
```

Press Enter for an optional value to keep its marker unchanged.

The command creates `src/proj_{PROJECT_NUMBER}_{PROJECT_PACKAGE}` and updates the root `README.md`, `pyproject.toml`, and `_config.yaml` project defaults.

### Options

- `--number INTEGER`: Required project number.
- `--package TEXT`: Required lowercase package component.
- `--title TEXT`: Required project title.
- `--ui-subtitle TEXT`: Required GitHub Pages subtitle.
- `--description TEXT`: Optional project description.
- `--deps DEP [DEP ...]`: Optional dependencies documented in the generated README.
- `--force`: Overwrite an existing project directory.
- `--silent`: Suppress progress logs.
- `--dry-run`: Show planned actions without creating or modifying files.
- `--help`: Show command usage.

Progress logs use timestamped, colored `INFO`, `WARN`, and `ERROR` levels with
centered action labels. Errors are always printed, including in silent mode.
