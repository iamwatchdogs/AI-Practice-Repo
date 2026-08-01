# AI Practice Repo

<div align="center">

[![CI](https://github.com/iamwatchdogs/AI-Practice-Repo/actions/workflows/ci.yaml/badge.svg)](https://github.com/iamwatchdogs/AI-Practice-Repo/actions/workflows/ci.yaml "goto ci workflow")
[![GitHub Pages](https://github.com/iamwatchdogs/AI-Practice-Repo/actions/workflows/gh-pages.yaml/badge.svg)](https://github.com/iamwatchdogs/AI-Practice-Repo/actions/workflows/gh-pages.yaml "goto gh-pages workflow")

</div>

<div align="center">

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![uv](https://img.shields.io/badge/uv-%23DE5FE9.svg?style=for-the-badge&logo=uv&logoColor=white)
![Zed](https://img.shields.io/badge/zedindustries-084CCF.svg?style=for-the-badge&logo=zedindustries&logoColor=white)

</div>

This is a sample repository where I practice and gain hands-on experience with a modern AI-engineering stack, from simple API requests to large-scale agentic applications for specific use cases.

## Index

You can check on each of the project from here,

<!-- INDEX STARTS HERE -->
- [Utility Package](./src/utils "goto utility package")
- [Project-1: Intro to LLM API](./src/proj_1_intro_to_llm_api "goto project-1 on github")
<!-- INDEX ENDS HERE -->

## Setup

### GenAI Project
This repo has a shared [`pyproject.toml`](https://github.com/iamwatchdogs/AI-Practice-Repo/blob/main/pyproject.toml) file across all the project, thus making it easily switch and execute between projects. So, if you cloned the repo and synced the uv dependencies, then you're good to go.

If you need some help, here're some steps:

- Start by [forking the repo](https://github.com/iamwatchdogs/AI-Practice-Repo/fork).

- Then clone the repo to your local system.

```bash
git clone https://github.com/<your-github-username>/AI-Practice-Repo.git

# If you prefer using ssh then,
# git clone git@github.com:<your-github-username>/AI-Practice-Repo.git

# If you prefer using gh-cli then
# gh repo clone <your-github-username>/AI-Practice-Repo
```

- Goto into the repo and sync with the uv dependencies

```bash
# Changing into the repo directory
cd AI-Practice-Repo

# Ensure you have installed `uv`
# And then sync the dependencies
uv sync
```

- Now, you can execute all the all the project that you can find with this practice repo.

```bash
# The scripts are in place an you can execute the following,
uv run proj_1

# I'll keep the same naming convention standard, so that you can check them all out using,
# `uv run proj_{0-9}*` pattern
```

> [!NOTE]
>
> To initialize a new project within this practice repo without disturbing the existing workflow, we have a [`create_new_project` utility](./src/utils).

### Jekyll for GitHub Pages

This repo uses the [bulma-clean-theme](https://github.com/chrisrhymes/bulma-clean-theme) remote theme to render this README (and the sub-project pages) as a GitHub Pages site. To preview it locally:

- Make sure you have [Ruby](https://www.ruby-lang.org/en/downloads/) installed.

- Install Jekyll and Bundler.

```bash
# If you don't have them yet,
gem install jekyll bundler
```

- Install the dependencies (from the `Gemfile` at the root of the repo).

```bash
bundle install
```

- Build the site and start the local server.

```bash
bundle exec jekyll serve --livereload
```

- Open the printed URL (usually <http://127.0.0.1:4000/>) in your browser. Any change to `_config.yaml` requires a full restart, while content changes are picked up automatically (or trigger a rebuild with `bundle exec jekyll build`).

> [!TIP]
> The local build uses the same `_includes`/`_layouts` overrides committed to this repo, so what you see locally matches the deployed GitHub Pages output.

## Contribution

Currently this is my own personal practice repo, that is being user for my own understanding and documentation. Therefore, no external contribution will be accepted at the moment. But you're free to fork and clone the repo for your own use since this is repo is licensed under MIT.

## License

This repo is licensed under [MIT License](https://github.com/iamwatchdogs/AI-Practice-Repo/blob/main/LICENSE "view license").
