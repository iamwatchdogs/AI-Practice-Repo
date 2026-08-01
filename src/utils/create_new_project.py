"""Create practice projects from the repository templates."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Final, Literal, TextIO, cast

if TYPE_CHECKING:
    from collections.abc import Sequence

PROJECT_PREFIX: Final[str] = "proj_"
INDEX_START: Final[str] = "<!-- INDEX STARTS HERE -->"
INDEX_END: Final[str] = "<!-- INDEX ENDS HERE -->"
TEMPLATES_DIR: Final[Path] = Path(__file__).resolve().parent / "templates"
MARKER_RE: Final[re.Pattern[str]] = re.compile(r"\{([A-Z][A-Z0-9_]*)\}|\[([^\]]+)\]")
REQUIRED_MARKERS: Final[tuple[str, ...]] = (
    "PROJECT_NUMBER",
    "PROJECT_PACKAGE",
    "PROJECT_TITLE",
    "UI_SUBTITLE",
)
LOG_COLORS: Final[dict[str, str]] = {
    "INFO": "\033[32m",
    "WARN": "\033[33m",
    "ERROR": "\033[31m",
}
RESET_COLOR: Final[str] = "\033[0m"
LogLevel = Literal["INFO", "WARN", "ERROR"]


class ProjectScaffoldError(Exception):
    """Raised when a project cannot be created or registered."""


def _error(message: str) -> ProjectScaffoldError:
    """Build a project-scaffolding error with a dynamic message.

    Args:
        message (str): Error message.

    Returns:
        ProjectScaffoldError: The configured error.

    """
    return ProjectScaffoldError(message)


@dataclass(frozen=True)
class _ProjectInput:
    """Validated project input values."""

    number: int
    package: str
    title: str
    ui_subtitle: str
    optional_values: dict[str, str]
    force: bool
    silent: bool
    dry_run: bool


def main(argv: Sequence[str] | None = None) -> None:
    """Create a project using command-line or interactive input.

    Args:
        argv (Sequence[str] | None): Arguments to parse. ``None`` uses the
            process arguments.

    Raises:
        SystemExit: When input is invalid or creation fails.

    """
    try:
        tokens = list(sys.argv[1:] if argv is None else argv)
        project_input = _interactive_input() if not tokens else _parse_args(tokens)
        _scaffold(project_input)
    except (ProjectScaffoldError, OSError) as exc:
        _log_message("ERROR", "Error", str(exc), force=True, stream=sys.stderr)
        raise SystemExit(1) from exc


def _parse_args(argv: Sequence[str]) -> _ProjectInput:
    """Parse required and optional command-line inputs.

    Args:
        argv (Sequence[str]): Command-line arguments.

    Returns:
        _ProjectInput: Parsed project input.

    """
    parser = argparse.ArgumentParser(
        description="Create a practice project from src/utils/templates.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Interactive mode:
  Run without arguments to enter the required values interactively. The script
  then prompts for each optional square-bracket template marker. Press Enter
  without a value to keep that marker unchanged.

Command-line examples:
  uv run create_new_project
  uv run create_new_project \\
    --number 2 \\
    --package intro_to_rag \\
    --title "Intro to RAG" \\
    --ui-subtitle "A retrieval-augmented generation project"
  uv run create_new_project \\
    --number 2 \\
    --package intro_to_rag \\
    --title "Intro to RAG" \\
    --ui-subtitle "A retrieval-augmented generation project" \\
    --description "Practice retrieval-augmented generation" \\
    --deps openai pydantic

The generated package is written to:
  src/proj_{PROJECT_NUMBER}_{PROJECT_PACKAGE}

The command also updates pyproject.toml, _config.yaml, and the root README.md
unless --dry-run is supplied. Use --silent to suppress progress logs.
""",
    )
    parser.add_argument(
        "--number",
        type=int,
        required=True,
        help="Required positive project number, for example 2.",
    )
    parser.add_argument(
        "--package",
        required=True,
        help="Required lowercase package component, for example intro_to_rag.",
    )
    parser.add_argument(
        "--title",
        required=True,
        help="Required human-readable project title.",
    )
    parser.add_argument(
        "--ui-subtitle",
        required=True,
        help="Required subtitle written to the GitHub Pages configuration.",
    )
    parser.add_argument(
        "--description",
        help="Optional value for the [PROJECT_DESCRIPTION] template marker.",
    )
    parser.add_argument(
        "--deps",
        nargs="*",
        help="Optional dependencies used to replace dependency template markers.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite the destination package if it already exists.",
    )
    parser.add_argument(
        "--silent",
        action="store_true",
        help="Suppress normal progress logs; errors are still shown.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show planned actions without creating or modifying files.",
    )
    args = parser.parse_args(argv)
    number = cast("int", args.number)
    package_value = cast("str", args.package)
    title = cast("str", args.title)
    ui_subtitle = cast("str", args.ui_subtitle)
    description = cast("str | None", args.description)
    deps = cast("list[str] | None", args.deps)
    if number < 1:
        raise _error("--number must be a positive integer")
    package = _validate_package(package_value)
    optional_values: dict[str, str] = {}
    if description is not None:
        optional_values["PROJECT_DESCRIPTION"] = description
    if deps:
        optional_values["deps"] = " ".join(deps)
    return _ProjectInput(
        number=number,
        package=package,
        title=title,
        ui_subtitle=ui_subtitle,
        optional_values=optional_values,
        force=cast("bool", args.force),
        silent=cast("bool", args.silent),
        dry_run=cast("bool", args.dry_run),
    )


def _interactive_input() -> _ProjectInput:
    """Prompt for required values and every optional template marker.

    Returns:
        _ProjectInput: Values entered by the user.

    """
    number_text = input("PROJECT_NUMBER (required): ").strip()
    package = input("PROJECT_PACKAGE (required): ").strip()
    title = input("PROJECT_TITLE (required): ").strip()
    ui_subtitle = input("UI_SUBTITLE (required): ").strip()
    if not number_text or not package or not title or not ui_subtitle:
        raise _error("All required inputs must be provided")
    try:
        number = int(number_text)
    except ValueError as exc:
        raise _error("PROJECT_NUMBER must be an integer") from exc
    if number < 1:
        raise _error("PROJECT_NUMBER must be positive")
    package = _validate_package(package)
    optional_values: dict[str, str] = {}
    for marker in _optional_markers():
        hint = " space-separated," if marker == "deps" else ""
        value = input(f"{marker} (optional,{hint} blank keeps marker): ")
        if value:
            optional_values[marker] = value
    return _ProjectInput(
        number,
        package,
        title,
        ui_subtitle,
        optional_values,
        force=False,
        silent=False,
        dry_run=False,
    )


def _optional_markers() -> tuple[str, ...]:
    """Return unique square-bracket markers found in all template files.

    Returns:
        tuple[str, ...]: Marker names in discovery order.

    """
    markers: list[str] = []
    for path in _template_files():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for match in MARKER_RE.finditer(text):
            marker = match.group(2)
            if marker and marker not in markers:
                markers.append(marker)
    return tuple(markers)


def _scaffold(project_input: _ProjectInput) -> None:
    """Create files and update repository metadata.

    Args:
        project_input (_ProjectInput): Validated project input.

    """
    repo_root = _find_repo_root(Path.cwd())
    module = f"{PROJECT_PREFIX}{project_input.number}_{project_input.package}"
    project_dir = repo_root / "src" / module
    if not project_input.dry_run:
        _create_project_dir(project_dir, force=project_input.force)
    _log(project_input, "Created", f"package ./src/{module}")
    replacements = _replacements(project_input)
    for source in _template_files():
        relative = source.relative_to(TEMPLATES_DIR)
        destination = project_dir / relative
        if not project_input.dry_run:
            destination.parent.mkdir(parents=True, exist_ok=True)
            _copy_template(source, destination, replacements)
        _log(project_input, "Added", f"{relative} file to the package")
    if not project_input.dry_run:
        _update_pyproject(repo_root, project_input.number, module)
    _log(project_input, "Registered", "package to pyproject.toml")
    if not project_input.dry_run:
        _update_config(repo_root, project_input, module)
    _log(project_input, "Registered", "package to _config.yaml")
    if not project_input.dry_run:
        _update_root_readme(
            repo_root, project_input.number, project_input.title, module
        )
    _log(project_input, "Updated", "repo root README.md index")
    _log(
        project_input,
        "Logging",
        "Dry run complete" if project_input.dry_run else "Package creation complete",
    )


def _log(project_input: _ProjectInput, action: str, message: object = "") -> None:
    """Print a progress message unless silent mode is enabled.

    Args:
        project_input (_ProjectInput): Current command options.
        action (str): Action label.
        message (object): Human-readable event message.

    """
    _log_message(
        "INFO",
        action,
        str(message),
        silent=project_input.silent,
    )


def _log_message(
    level: LogLevel,
    action: str,
    message: str,
    *,
    silent: bool = False,
    force: bool = False,
    stream: TextIO = sys.stdout,
) -> None:
    """Write a consistently formatted colored log message.

    Args:
        level (LogLevel): Log severity.
        action (str): Action label centered in a 12-character field.
        message (str): Human-readable event message.
        silent (bool): Suppress non-forced logs.
        force (bool): Emit the log even when silent mode is enabled.
        stream (object): Output stream receiving the log.

    """
    if silent and not force:
        return
    timestamp = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")
    color = LOG_COLORS[level]
    formatted_action = f"{action:^12}"
    print(
        f"[{timestamp}] [{color}{level}{RESET_COLOR}] ::{formatted_action}:: {message}",
        file=stream,
    )


def _template_files() -> tuple[Path, ...]:
    """Return every file below the template directory.

    Returns:
        tuple[Path, ...]: Template files in stable path order.

    """
    return tuple(sorted(path for path in TEMPLATES_DIR.rglob("*") if path.is_file()))


def _copy_template(
    source: Path, destination: Path, replacements: dict[str, str]
) -> None:
    """Copy one template and substitute UTF-8 text markers when possible.

    Args:
        source (Path): Source template file.
        destination (Path): Destination file.
        replacements (dict[str, str]): Marker replacements.

    """
    raw = source.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        destination.write_bytes(raw)
        return
    for marker, replacement in replacements.items():
        text = text.replace(marker, replacement)
    destination.write_text(text, encoding="utf-8")


def _replacements(project_input: _ProjectInput) -> dict[str, str]:
    """Build required and supplied optional marker replacements.

    Args:
        project_input (_ProjectInput): Project input values.

    Returns:
        dict[str, str]: Exact marker-to-value replacements.

    """
    replacements = {
        "{PROJECT_NUMBER}": str(project_input.number),
        "{PROJECT_PACKAGE}": project_input.package,
        "{PROJECT_TITLE}": project_input.title,
        "{UI_SUBTITLE}": project_input.ui_subtitle,
    }
    for marker, value in project_input.optional_values.items():
        replacements[f"[{marker}]"] = value
    if "deps" in project_input.optional_values:
        deps = project_input.optional_values["deps"].split()
        replacements["- dep1\n- dep2"] = "\n".join(f"- {dep}" for dep in deps)
        replacements["uv add [deps]"] = "uv add " + " ".join(deps)
        replacements["pip install [deps]"] = "pip install " + " ".join(deps)
    return replacements


def _find_repo_root(start: Path) -> Path:
    """Find the repository root from a starting directory.

    Args:
        start (Path): Directory from which to search upward.

    Returns:
        Path: Repository root.

    """
    for candidate in (start, *start.parents):
        if (candidate / "pyproject.toml").is_file() and (candidate / "src").is_dir():
            return candidate
    raise _error("Could not locate the repository root")


def _validate_package(package: str) -> str:
    """Validate the package component used in the generated module name.

    Args:
        package (str): Package component.

    Returns:
        str: Validated package component.

    """
    if not re.fullmatch(r"[a-z][a-z0-9_]*", package):
        raise _error(
            "PROJECT_PACKAGE must start with a lowercase letter and contain "
            "only lowercase letters, numbers, and underscores"
        )
    return package


def _create_project_dir(project_dir: Path, *, force: bool) -> None:
    """Create the destination directory, optionally replacing it.

    Args:
        project_dir (Path): Destination directory.
        force (bool): Whether an existing directory may be removed.

    """
    if project_dir.exists():
        if not force:
            raise _error(
                f"Project directory already exists: {project_dir}. Use --force."
            )
        shutil.rmtree(project_dir)
    project_dir.mkdir(parents=True)


def _update_pyproject(repo_root: Path, number: int, module: str) -> None:
    """Register the generated module in ``pyproject.toml``.

    Args:
        repo_root (Path): Repository root.
        number (int): Project number.
        module (str): Full generated module name.

    """
    path = repo_root / "pyproject.toml"
    content = path.read_text(encoding="utf-8")
    if f'"src/{module}"' not in content:
        content = _insert_array_value(
            content, "tool.hatch.build.targets.wheel", "src/" + module
        )
    if f'"{module}"' not in content:
        content = _insert_array_value(content, "tool.mypy", module)
    script_key = f"proj_{number}"
    if f"{script_key} =" not in content:
        content = _insert_script(content, script_key, f"{module}.main:main")
    path.write_text(content, encoding="utf-8")


def _insert_array_value(content: str, section: str, value: str) -> str:
    """Insert a quoted value into a multiline TOML array.

    Args:
        content (str): TOML content.
        section (str): Section containing the array.
        value (str): Value to insert.

    Returns:
        str: Updated TOML content.

    """
    lines = content.splitlines()
    section_index = _find_section(lines, section)
    section_end = next(
        (
            index
            for index in range(section_index + 1, len(lines))
            if lines[index].strip().startswith("[")
            and lines[index].strip().endswith("]")
        ),
        len(lines),
    )
    array_index = next(
        (
            index
            for index in range(section_index + 1, section_end)
            if lines[index].strip().startswith("packages = [")
        ),
        None,
    )
    if array_index is None:
        message = f"packages array missing from [{section}]"
        raise _error(message)
    array_line = lines[array_index]
    if array_line.rstrip().endswith("]"):
        closing_bracket = array_line.rfind("]")
        values = array_line[:closing_bracket].rstrip()
        separator = "" if values.endswith("[") else ", "
        lines[array_index] = (
            values + separator + f'"{value}"' + array_line[closing_bracket:]
        )
        return _join_lines(lines, trailing_newline=content.endswith("\n"))
    end = next(
        (
            index
            for index in range(array_index + 1, section_end)
            if lines[index].strip() == "]"
        ),
        None,
    )
    if end is None:
        message = f"packages array is unterminated in [{section}]"
        raise _error(message)
    previous = lines[end - 1]
    if previous.strip() and not previous.rstrip().endswith(","):
        lines[end - 1] = previous.rstrip() + ","
    indent = previous[: len(previous) - len(previous.lstrip())]
    lines.insert(end, f'{indent}"{value}"')
    return _join_lines(lines, trailing_newline=content.endswith("\n"))


def _insert_script(content: str, key: str, value: str) -> str:
    """Insert a console script into the project scripts section.

    Args:
        content (str): TOML content.
        key (str): Script name.
        value (str): Script target.

    Returns:
        str: Updated TOML content.

    """
    lines = content.splitlines()
    section_index = _find_section(lines, "project.scripts")
    insert_at = section_index + 1
    while insert_at < len(lines):
        if not lines[insert_at].strip() or lines[insert_at].startswith("["):
            break
        insert_at += 1
    lines.insert(insert_at, f'{key} = "{value}"')
    return _join_lines(lines, trailing_newline=content.endswith("\n"))


def _find_section(lines: list[str], section: str) -> int:
    """Find a TOML section header.

    Args:
        lines (list[str]): TOML lines.
        section (str): Section name.

    Returns:
        int: Header index.

    """
    header = f"[{section}]"
    for index, line in enumerate(lines):
        if line.strip() == header:
            return index
    message = f"Section [{section}] not found"
    raise _error(message)


def _update_config(repo_root: Path, project_input: _ProjectInput, module: str) -> None:
    """Add the project page defaults block to ``_config.yaml``.

    Args:
        repo_root (Path): Repository root.
        project_input (_ProjectInput): Project values.
        module (str): Full generated module name.

    """
    path = repo_root / "_config.yaml"
    content = path.read_text(encoding="utf-8")
    scope_path = f"src/{module}"
    if f'path: "{scope_path}"' in content:
        return
    block = (
        "  - scope:\n"
        f'      path: "{scope_path}"\n'
        '      type: "pages"\n'
        "    values:\n"
        f'      subtitle: "{_yaml_value(project_input.ui_subtitle)}"\n'
        f"      hero_link: https://github.com/iamwatchdogs/AI-Practice-Repo/tree/main/{scope_path}\n"
    )
    if "defaults:\n" not in content or "plugins:\n" not in content:
        raise _error("Could not locate the defaults section in _config.yaml")
    lines = content.splitlines()
    plugins_index = lines.index("plugins:")
    insert_at = plugins_index
    while insert_at > 0 and not lines[insert_at - 1].strip():
        insert_at -= 1
    lines[insert_at:insert_at] = block.rstrip("\n").splitlines()
    content = _join_lines(lines, trailing_newline=content.endswith("\n"))
    path.write_text(content, encoding="utf-8")


def _yaml_value(value: str) -> str:
    """Escape a value used inside a YAML double-quoted scalar.

    Args:
        value (str): User-provided value.

    Returns:
        str: Escaped YAML scalar content.

    """
    return value.replace("\\", "\\\\").replace('"', '\\"')


def _update_root_readme(repo_root: Path, number: int, title: str, module: str) -> None:
    """Insert the project link between the root README markers.

    Args:
        repo_root (Path): Repository root.
        number (int): Project number.
        title (str): Project title.
        module (str): Full generated module name.

    """
    path = repo_root / "README.md"
    content = path.read_text(encoding="utf-8")
    link = (
        f"- [Project-{number}: {title}](./src/{module} "
        f'"goto project-{number} on github")'
    )
    if link in content:
        return
    if INDEX_START not in content or INDEX_END not in content:
        raise _error("README index markers are missing")
    lines = content.splitlines()
    start = lines.index(INDEX_START)
    end = lines.index(INDEX_END)
    insert_at = start + 1
    for index in range(start + 1, end):
        match = re.search(r"Project-(\d+):", lines[index])
        if match and int(match.group(1)) < number:
            insert_at = index + 1
    lines.insert(insert_at, link)
    path.write_text(
        _join_lines(lines, trailing_newline=content.endswith("\n")),
        encoding="utf-8",
    )


def _join_lines(lines: list[str], *, trailing_newline: bool) -> str:
    """Join lines while preserving an existing final newline.

    Args:
        lines (list[str]): Lines to join.
        trailing_newline (bool): Whether the source ended with a newline.

    Returns:
        str: Joined content.

    """
    result = "\n".join(lines)
    return result + "\n" if trailing_newline else result


if __name__ == "__main__":
    main()
