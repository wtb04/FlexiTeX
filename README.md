<picture>
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/wtb04/FlexiTeX/refs/heads/main/misc/FlexiTeX-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/wtb04/FlexiTeX/refs/heads/main/misc/FlexiTeX-dark.svg">
  <img alt="FlexiTeX Logo" height="100">
</picture>

FlexiTeX is a command-line tool for restructuring and splitting large LaTeX projects.  
It enables users to define custom rules for organizing LaTeX documents, manages figures and file paths, and can visualize document structure.  
The tool is intended for collaborative writing, sharing, or reorganizing complex LaTeX documents.

## Installation

From the root directory run:

```sh
pip install .
```

## Quick Start

1. Prepare your LaTeX project and a config file (see [`example-config.yml`](example-config.yml)).
2. Run FlexiTeX:
    ```sh
    flexitex -c example-config.yml
    ```

## Usage

```sh
flexitex [-c CONFIG] [--debug] [-vo] [-vf]
         [-if INPUT_FOLDER] [-im INPUT_MAIN]
         [-of OUTPUT_FOLDER] [-om OUTPUT_MAIN]
         [-fig FIGURE_FOLDER]
```

| Option                        | Required | Argument     | Description                                                        |
| ----------------------------- | -------- | ------------ | ------------------------------------------------------------------ |
| `-c`, `--config`              | No       | Path to YAML | Path to config file (default: `config.yml`)                        |
| `--debug`, `-d`               | No       | None         | Enable debug output during parsing                                 |
| `-vo`, `--visualize-original` | No       | None         | Show initial AST as Graphviz PDF (before applying splitting rules) |
| `-vf`, `--visualize-final`    | No       | None         | Show final AST as Graphviz PDF (after applying splitting rules)    |
| `-if`, `--input-folder`       | No       | Path         | Override: input folder (e.g., `./input`)                           |
| `-im`, `--input-main`         | No       | Filename     | Override: input main file (e.g., `main.tex`)                       |
| `-of`, `--output-folder`      | No       | Path         | Override: output folder (e.g., `./output`)                         |
| `-om`, `--output-main`        | No       | Filename     | Override: output main file (e.g., `output.tex`)                    |
| `-fig`, `--figure-folder`     | No       | Path         | Override: folder for figures (e.g., `figs/`)                       |

## Configuration

See [`example-config.yml`](example-config.yml) for a template.

## Example Repository

For a working demonstration of collaborative workflows using FlexiTeX, see the [FlexiTeX-Example repository](https://github.com/wtb04/FlexiTeX-Example).  
It shows how multiple users can maintain custom LaTeX styles across branches with automated synchronization via GitHub Actions.

## License

MIT License. See [LICENSE](LICENSE).
