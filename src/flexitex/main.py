import argparse
import os

from graphviz import Source

from flexitex.core.config import Config
from flexitex.core.processor import LatexProcessor
from flexitex.core.writer import OutputWriter
from flexitex.flexiast.structure import Structure
from flexitex.generators.latex_generator import LatexGenerator
from flexitex.generators.dot_generator import DotGenerator


def run_main(config_path: str, debug: bool, visualize: bool):
    config = Config(path=config_path)

    processor = LatexProcessor(config.input_file, debug=debug)
    ast = processor.parse()

    if visualize:
        dot = DotGenerator()
        dot_str = dot.to_dot(ast, hide_before_document=True)
        graph = Source(dot_str, format="pdf")
        graph.view(cleanup=True)


    structure = Structure(
        output_path=config.output_folder,
        output_main_file=config.output_main_file,
        rules=config.structure_rules
    )

    generator = LatexGenerator(structure)
    files = generator.to_latex(ast)

    writer = OutputWriter(config.output_folder)
    writer.write_all(files, clear_output=True)


def main():
    parser = argparse.ArgumentParser(description="FlexiTeX – LaTeX structure splitter and AST tool")
    parser.add_argument(
        "-c", "--config", default="config.yml", help="Path to config YAML file"
    )
    parser.add_argument(
        "--debug", action="store_true", help="Enable debug output during parsing"
    )
    parser.add_argument(
        "--visualize", action="store_true", help="Print Graphviz DOT of AST"
    )

    args = parser.parse_args()
    run_main(args.config, args.debug, args.visualize)


if __name__ == "__main__":
    main()
