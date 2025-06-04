import argparse
import os

from graphviz import Source

from flexitex.core.config import Config
from flexitex.core.graphics_move_manager import GraphicsMoveManager
from flexitex.core.processor import LatexProcessor
from flexitex.core.writer import OutputWriter
from flexitex.flexiast.structure import Structure
from flexitex.generators.latex_generator import LatexGenerator
from flexitex.generators.dot_generator import DotGenerator


def run_main(config_path: str, debug: bool, visualize_original: bool, visualize_final: bool):
    config = Config(path=config_path)

    processor = LatexProcessor(
        config.input_folder, config.input_main_file, debug=debug)
    ast = processor.parse()

    if visualize_original:
        dot = DotGenerator()
        dot_str = dot.to_dot(ast, hide_before_document=True)
        graph = Source(dot_str, format="pdf")
        graph.view("original", cleanup=True)

    graphics_mover = GraphicsMoveManager(
        config.input_folder, config.output_folder, config.output_figure_folder)
    ast = graphics_mover.detect_moves(ast)

    structure = Structure(
        output_path=config.output_folder,
        output_main_file=config.output_main_file,
        rules=config.structure_rules
    )

    generator = LatexGenerator(structure)
    files = generator.to_latex(ast)

    writer = OutputWriter(config.output_folder, debug=debug)
    writer.write_all(files, clear_output=True)
    graphics_mover.move_files()

    if visualize_final:
        dot = DotGenerator()
        dot_str = dot.to_dot(ast, hide_before_document=True)
        graph = Source(dot_str, format="pdf")
        graph.view("final", cleanup=True)


def main():
    parser = argparse.ArgumentParser(
        description="FlexiTeX - LaTeX project style transformation tool")
    parser.add_argument(
        "-c", "--config", default="config.yml", help="Path to config YAML file"
    )
    parser.add_argument(
        "--debug", action="store_true", help="Enable debug output during parsing"
    )
    parser.add_argument(
        "-vo", "--visualize-original", action="store_true", help="Display Graphviz pdf of initial AST"
    )
    parser.add_argument(
        "-vf", "--visualize-final", action="store_true", help="Display Graphviz pdf of final AST"
    )

    args = parser.parse_args()
    run_main(args.config, args.debug,
             args.visualize_original, args.visualize_final)


if __name__ == "__main__":
    main()
