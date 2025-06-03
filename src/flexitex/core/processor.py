from flexitex.parsing.preprocess import PreProcess
from flexitex.parsing.parser import LatexParser
from flexitex.flexiast.builder import to_ast


class LatexProcessor:
    def __init__(self, input_folder: str, input_main_file: str, debug: bool = False):
        self.input_folder = input_folder
        self.input_file = input_main_file
        self.debug = debug

    def parse(self):
        preprocessed = PreProcess.pre_process(self.input_folder, self.input_file)
        nodes = LatexParser.get_nodes_from_string(preprocessed)
        ast = to_ast(nodes, preprocessed)

        if self.debug:
            print(nodes)
            print(ast)

        return ast
