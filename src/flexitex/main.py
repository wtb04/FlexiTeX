import argparse
import os

from graphviz import Source

from flexitex.core.config import Config
from flexitex.core.move_manager import MoveManager
from flexitex.core.processor import LatexProcessor
from flexitex.core.writer import OutputWriter
from flexitex.flexiast.structure import Structure
from flexitex.generators.latex_generator import LatexGenerator
from flexitex.generators.dot_generator import DotGenerator


def run_main(config: Config, debug: bool, visualize_original: bool, visualize_final: bool):
    processor = LatexProcessor(
        config.input_folder, config.input_main_file, debug=debug)
    ast = processor.parse()

    if visualize_original:
        dot = DotGenerator()
        dot_str = dot.to_dot(ast, hide_before_document=True)
        graph = Source(dot_str, format="pdf")
        graph.view("original", cleanup=True)

    move_manager = MoveManager(
        config.input_folder, config.output_folder, config.output_figure_folder)
    ast = move_manager.detect_moves(ast)

    structure = Structure(
        output_path=config.output_folder,
        output_main_file=config.output_main_file,
        rules=config.structure_rules
    )

    generator = LatexGenerator(structure)
    files = generator.to_latex(ast)

    writer = OutputWriter(config.output_folder, debug=debug)
    writer.write_all(files, clear_output=True)
    move_manager.move_files()

    if visualize_final:
        dot = DotGenerator()
        dot_str = dot.to_dot(ast, hide_before_document=True)
        graph = Source(dot_str, format="pdf")
        graph.view("final", cleanup=True)


def main():
    parser = argparse.ArgumentParser(
        description="FlexiTeX - LaTeX project style transformation tool")

    # Configuration file
    parser.add_argument(
        "-c", "--config", default="config.yml", help="Path to YAML configuration file"
    )

    # Overrides for config fields
    parser.add_argument(
        "-if", "--input-folder", help="Override: input folder (relative or absolute)"
    )
    parser.add_argument(
        "-im", "--input-main", help="Override: input main file (e.g., main.tex)"
    )
    parser.add_argument(
        "-of", "--output-folder", help="Override: output folder (relative or absolute)"
    )
    parser.add_argument(
        "-om", "--output-main", help="Override: output main file (e.g., main.tex)"
    )
    parser.add_argument(
        "-fig", "--figure-folder", help="Override: folder where figures should be written"
    )

    # Debugging and visualization
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Enable debug output during parsing"
    )
    parser.add_argument(
        "-vo", "--visualize-original", action="store_true", help="Display Graphviz PDF of the initial AST"
    )
    parser.add_argument(
        "-vf", "--visualize-final", action="store_true", help="Display Graphviz PDF of the final AST"
    )

    args = parser.parse_args()

    config = Config(path=args.config)
    config.override(
        input_folder=args.input_folder,
        input_main=args.input_main,
        output_folder=args.output_folder,
        output_main=args.output_main,
        figure_folder=args.figure_folder,
    )

    run_main(config=config, debug=args.debug,
             visualize_original=args.visualize_original,
             visualize_final=args.visualize_final)


if __name__ == "__main__":
    main()
