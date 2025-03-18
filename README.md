[![CI Status][ci-shield]][ci-url]
[![Coverage][coverage-shield]][coverage-url]
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]


<br />
<div align="center">
  <a href="https://github.com/parkermmr/CAB320A1">
    <img src="database/images/logo.svg" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">CAB320 Assignment 1 - Search</h3>

  <p align="center">
    An introductory project optimizing search AI.
    <br />
    <a href="https://github.com/parkermmr/CAB320A1"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/parkermmr/CAB320A1">View Demo</a>
    &middot;
    <a href="https://github.com/parkermmr/CAB320A1/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://https://github.com/parkermmr/CAB320A1/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li>
      <a href="#usage">Usage</a>
      <ul>
        <li><a href="#compendium-ci">Compendium CI</a></li>
      </ul>
    </li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

## About The Project


### Built With

<p align="center">
  
- [![Python][python]][python-url]
- [![Jupyter][jupyter]][jupyter-url]
- [![Git][git]][git-url]
- [![GitHub Actions][github-actions]][github-actions-url]
- [![Docker][docker]][docker-url]

</p>
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started
This project encompasses a weighted search solver AI system build specifically for solving the 1982 - IBM computer game, Sokoban.

### Prerequisites
This project relies on Python, Poetry, and Git. Apart from those, that's it! It is important that the correct versions of Python and Poetry are installed, otherwise all the dependencies are managed in the `pyptoject.toml` file at the root directory. The below version are relvant to the project:
```python
python=^3.13
poetry=^2.0.0
```

Another optional non-python dependency is the VSCode extension - `Markdown Preview Enhanced` by Yiyi Wang. This extension allows for HTML, CSS, and JS to be rendered inside `.md` files and compiled in to representive PDFs.

### Installation
As aforementioned, all dependencies - other than critical dependencies - are managed within the `pyproject.yaml` at the project root. It is recommended where practical Poetry is used within a automatically generated `venv` to run any testing, linting, and project scripts - with the sole exception to the `gui_sokoban.py` module file which relies on `tk` a Python GUI interface which benefits from running on the global Python namespace. With that being said, the project dependencies can be installed through the CLI as such:

```bash
poetry lock && poetry install

# Alternatively for a pip installation on a venv or global namespace
pip install --upgrade pip && pip install
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage
To run the Python GUI interface for the Sokoban application, it is recommended that it is ran on a global Python namespace. From the project root after the installation steps have been followed run the below:

```bash
python3 -m src.gui_sokoban

# Alternatively if running inside a poetry venv
poetry run python3 -m src.gui_sokoban
```

### Compendium CI
The current workflow being used is a Compendium CI Python Poetry pipeline with comprehensive checks for testing, linting, style, code security and structure. Compendium is a GitHub specific CI suite fully managed [here][compendium]. It is important that before any pushes are made the code quality checks and reformatting are ran. This can be done with the following commands:
```bash
poetry run black src && poetry run isort src
```
This will ensure the pipeline completes successfully and all code is to an appropriate format standard. For more information on the linting configuration seek out the `pyproject.toml` configuration under `[tools.black]` & `[tools.isort]` as well as the `.flake8` configuration file.

### Acknowledgments:

<a href="https://github.com/parkermmr/CAB320A1/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=parkermmr/CAB320A1" alt="contrib.rocks image" />
</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

[ci-shield]: https://img.shields.io/github/actions/workflow/status/parkermmr/cab320a1/compendium.yml?branch=main&style=for-the-badge
[ci-url]: https://github.com/parkermmr/cab320a1/actions/workflows/compendium.yml
[coverage-shield]: https://img.shields.io/codecov/c/github/parkermmr/cab320a1?style=for-the-badge
[coverage-url]: https://codecov.io/gh/parkermmr/cab320a1
[contributors-shield]: https://img.shields.io/github/contributors/parkermmr/CAB320A1.svg?style=for-the-badge
[contributors-url]: https://github.com/parkermmr/CAB320A1/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/parkermmr/CAB320A1.svg?style=for-the-badge
[forks-url]: https://github.com/parkermmr/CAB320A1/network/members
[stars-shield]: https://img.shields.io/github/stars/parkermmr/CAB320A1.svg?style=for-the-badge
[stars-url]: https://github.com/parkermmr/CAB320A1/stargazers
[issues-shield]: https://img.shields.io/github/issues/parkermmr/CAB320A1.svg?style=for-the-badge
[issues-url]: https://github.com/parkermmr/CAB320A1/issues
[python]: https://img.shields.io/badge/python-FFE873?style=for-the-badge&logo=python&logoColor
[python-url]: https://www.python.org/
[jupyter]: https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=Jupyter&logoColor=white
[jupyter-url]: https://jupyter.org/
[git]: https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white
[git-url]: https://git-scm.com/
[github-actions]: https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=GitHub%20Actions&logoColor=white
[github-actions-url]: https://github.com/features/actions
[docker]: https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=Docker&logoColor=white
[docker-url]: https://www.docker.com/
[compendium]: https://github.com/parkermmr/compendium