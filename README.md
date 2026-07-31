# AI Practice Repo

<div align="center">

[![CI](https://github.com/iamwatchdogs/AI-Practice-Repo/actions/workflows/ci.yaml/badge.svg)](https://github.com/iamwatchdogs/AI-Practice-Repo/actions/workflows/ci.yaml "goto ci workflow")

</div>

<div align="center">

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![uv](https://img.shields.io/badge/uv-%23DE5FE9.svg?style=for-the-badge&logo=uv&logoColor=white)
![Zed](https://img.shields.io/badge/zedindustries-084CCF.svg?style=for-the-badge&logo=zedindustries&logoColor=white)

</div>

This is sample repo where I practice and get some hands on "modern" AI-Engineering tech stack i.e., applications developed over API requests to commercial/local LLMs scaling from a simple API request to large scale agentic application with specific usecases.

## Index

You can check on each of the project from here,

- [Project-1: OpenAI Compatible API](./src/proj_1_openai_cmpt_api "goto project-1 on github")

## Setup

This repo has a shared [`pyproject.toml`](https://github.com/iamwatchdogs/AI-Practice-Repo/blob/main/pyproject.toml "view pyproject.toml") file across all the project, thus making it easily switch and execute between projects. So, if you cloned the repo and synced the uv dependencies, then you're good to go.

If you need some help, here're some steps:

- Start by [forking the repo](https://github.com/iamwatchdogs/AI-Practice-Repo/fork "fork the repo").

- Then clone the repo to your local system and change the directory into the repo.

```bash
git clone https://github.com/<your-github-username>/AI-Practice-Repo.git

# If you prefer using ssh then,
# git clone git@github.com:<your-github-username>/AI-Practice-Repo.git

# If you prefer using gh-cli then,
# gh repo clone <your-github-username>/AI-Practice-Repo

# Change into the repo directory
cd AI-Practice-Repo
```

- Ensure you have [uv](https://docs.astral.sh/uv/getting-started/installation/) installed and then sync the dependencies

```bash
# Sync the dependencies
uv sync
```

- Now, you can execute all the all the project that you can find with this practice repo.

```bash
# The scripts are in place an you can execute the following,
uv run proj_1

# I'll keep the same naming convention standard, so that you can check them all out using,
# uv run proj_{0-9}*
```

## Contribution

Currently this is my own personal practice repo, that is being user for my own understanding and documentation. Therefore, no external contribution will be accepted at the moment. But you're free to fork and clone the repo for your own use since this is repo is licensed under MIT.

## License

This repo is licensed under [MIT License](https://github.com/iamwatchdogs/AI-Practice-Repo/blob/main/LICENSE "view license").
