# Long run simulation of volcanic eruptions

<sup>Latest version: v0.1.0</sup> <!-- x-release-please-version -->

> [!WARNING]
>
> This README reflects the changes made to the main branch. For the most up to date
> documentation about the version you are using, see the README at the relevant tag.

This repository contains the design and setup for running long (>100yr) volcanic
eruption simulations in the CESM2 climate model. Eruptions are synthetic and designed to
both represent realistic (historical) eruptions and to cover a wide range of magnitudes.
The goal of the project is to resolve the tail of the temperature perturbations from the
eruptions well.

## Install

To install the project you must clone the repository. If you have [mise] installed
(recommended), this will install and set up the correct python version as a virtual
environment into `./.venv/`. If you do not wish to use [mise], [poetry] will by default
also create a virtual environment with an available python runtime.

```bash
git clone git@github.com:engeir/volcano-long-run.git
cd volcano-long-run
# poetry can be installed from pipx, as `pipx install poetry`. See https://python-poetry.org/docs/#installation
poetry install
```

> [!NOTE]
>
> The repository and project is named volcano-long-run, but the package name is `vlr`,
> just to make it shorter when importing.

After the `poetry install` command succeeds, you can check that everything is working by
running

<!-- x-release-please-start-version -->

```console
$ poetry run vlr
Hello, this is vlr at version v0.1.0!
```

<!-- x-release-please-end -->

## Usage

So far, only the welcome message at `poetry run vlr` is implemented. More will come!

[poetry]: https://python-poetry.org
[mise]: https://mise.jdx.dev/
