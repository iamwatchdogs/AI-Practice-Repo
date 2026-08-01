"""Repository-wide utility programs and scripts.

This is a utility package used across the repository. It contains reusable
programs and scripts that reduce repeated manual work when maintaining and
extending the practice projects.

The package currently consists of the `create_new_project` module/script.
This module initializes a new practice project from the templates in
`src/utils/templates`, substitutes the details provided by the user, copies
the package files, and registers the project in the repository metadata.

Important functions in `create_new_project` include:

main(argv: Sequence[str] | None) -> None
    Entry point for command-line and interactive execution. It validates the
    input mode and starts the project creation workflow.

_parse_args(argv: Sequence[str]) -> _ProjectInput
    Parses the required and optional command-line arguments.

_interactive_input() -> _ProjectInput
    Collects the required project details and optional template values through
    interactive prompts.

_scaffold(project_input: _ProjectInput) -> None
    Creates `src/proj_{PROJECT_NUMBER}_{PROJECT_PACKAGE}`, copies all
    template files, and updates the repository metadata files.

_copy_template(source: Path, destination: Path, replacements: dict[str, str])
    Copies a template file and replaces the required and supplied optional
    markers with the user's project details.

_update_pyproject(repo_root: Path, number: int, module: str) -> None
    Registers the generated package in the Hatch wheel packages, mypy package
    list, and project console scripts.

_update_config(repo_root: Path, project_input: _ProjectInput, module: str)
    Adds the generated project's page configuration under the `defaults`
    section of `_config.yaml`.

_update_root_readme(repo_root: Path, number: int, title: str, module: str)
    Adds the generated project to the root README index between its markers.
"""
