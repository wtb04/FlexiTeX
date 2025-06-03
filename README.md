# FlexiTeX

<picture>
  <source srcset="misc/FlexiTeX-dark.svg" media="(prefers-color-scheme: dark)">
  <img src="misc/FlexiTeX-light.svg" alt="FlexiTeX Logo" height="100">
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
```

| Option                    | Required | Argument         | Description                                 |
|---------------------------|----------|------------------|---------------------------------------------|
| `-c`, `--config`          | No       | Path to YAML     | Path to config file (default: `config.yml`) |
| `--debug`                 | No       | None             | Enable debug output during parsing          |
| `-vo`, `--visualize-original` | No   | None             | Show initial AST as Graphviz PDF            |
| `-vf`, `--visualize-final`    | No   | None             | Show final AST as Graphviz PDF              |

## Configuration

See [`example-config.yml`](example-config.yml) for a template.  
Key sections:

-   `structure`: Rules for splitting and naming output files
-   `input`: Input folder and main file
-   `output`: Output folder, main file, and figure folder

## License

MIT License. See [LICENSE](LICENSE).
