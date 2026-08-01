# Project-{PROJECT_NUMBER}: {PROJECT_TITLE}

[PROJECT_DESCRIPTION]

## Dependencies

This project requires following dependencies,

- dep1
- dep2

These dependencies have been installed using the `uv` package manager which has a shared environment across all projects,

```bash
uv add [deps]
```

<details>
<summary>
For `venv` users
</summary>

[venv user description]

```bash
# Create an venv
python -m venv .venv

# activate the environment
./.venv/bin/activate

# For windows based system, it would be
# .\venv\Scripts\activate.bat   if you're using powershell
# .\venv\Scripts\Activate.ps1   if you're using cmd
# source venv/Scripts/activate  if you're using git-bash/wsl

# Installing dependencies
pip install [deps]

# (Optional) you can save the dependencies into requirements.txt
pip freeze > requirements.txt
```

</details>

[DEPENDENCY_REQUIREMENT_EXPLANATION]

## Implementation

Here's a small brief of implementation in few words:

- step1
- step2

## Sample output:

You can set the relevant environmental variable in the `.env` file as suggested in the `.env.example` file and
use the following command to achieve similar results,

```bash
# Ensure you have previous synced the dependencies of the repo
uv run proj_{PROJECT_NUMBER}
```

<details>
<summary>
For `venv` users
</summary>

To run the project using `venv` environment, you can use the following commands:

```bash
# If you're within `proj_{PROJECT_NUMBER}_{PROJECT_PACKAGE}` dir
python main.py

# If you're within root of the repo
python src/proj_{PROJECT_NUMBER}_{PROJECT_PACKAGE}/main.py

# If you want to execute it as a library module then,
PYTHONPATH=src python -m proj_{PROJECT_NUMBER}_{PROJECT_PACKAGE}.main
```

</details>

Here's the sample output,

[asciicinema]

<details>
<summary>
Sample Result
</summary>

~~~text
sample output
~~~

</details>
