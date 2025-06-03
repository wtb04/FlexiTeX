from pylatexenc.latexwalker import LatexWalker
from pylatexenc.macrospec import MacroSpec, EnvironmentSpec
import pylatexenc


class LatexParser:
    _context = None

    @staticmethod
    def _initialize_context():
        if LatexParser._context is not None:
            return

        ctx = pylatexenc.latexwalker.get_default_latex_context_db()

        ctx.add_context_category(
            None,
            prepend=True,
            macros=[MacroSpec('caption', args_parser='{')],
            environments=[EnvironmentSpec('minipage', args_parser='{')]
        )

        LatexParser._context = ctx

    @staticmethod
    def get_nodes_from_string(latex_str: str):
        LatexParser._initialize_context()
        walker = LatexWalker(latex_str, latex_context=LatexParser._context)
        nodes, _, _ = walker.get_latex_nodes(pos=0)
        return nodes

    @staticmethod
    def get_nodes_from_file(filename: str):
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        return LatexParser.get_nodes_from_string(content)
