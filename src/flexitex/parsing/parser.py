from pylatexenc.latexwalker import LatexWalker
from pylatexenc.macrospec import MacroSpec, EnvironmentSpec, VerbatimArgsParser
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
            macros=[MacroSpec('caption', args_parser='{'), MacroSpec('AtBeginDocument', args_parser='{'), MacroSpec('setcopyright', args_parser='{'), MacroSpec('copyrightyear', args_parser='{'), MacroSpec('acmYear', args_parser='{'),
                    MacroSpec('acmPrice', args_parser='{'), MacroSpec('acmISBN', args_parser='{'), MacroSpec(
                        'acmDOI', args_parser='{'), MacroSpec('acmConference', args_parser='[{{{'), MacroSpec('crefname', args_parser='{{{'),
                    MacroSpec('Crefname', args_parser='{{{'), MacroSpec('newcounter', args_parser='{'), MacroSpec(
                        'refstepcounter', args_parser='{'), MacroSpec('author', args_parser='{'), MacroSpec('affiliation', args_parser='{'),
                    MacroSpec('institution', args_parser='{'), MacroSpec('streetaddress', args_parser='{'), MacroSpec(
                        'city', args_parser='{'), MacroSpec('postcode', args_parser='{'), MacroSpec('country', args_parser='{'),
                    MacroSpec('country', args_parser='{'), MacroSpec('newcolumntype', args_parser='{[{'), MacroSpec('email', args_parser='{'), MacroSpec(
                        'bibliographystyle', args_parser='{'), MacroSpec('rqlabel', args_parser='{'), MacroSpec('cref', args_parser='{'), MacroSpec('subfigure', args_parser='{'),
                    MacroSpec('Cref', args_parser='{'), MacroSpec(macroname='verb', args_parser=VerbatimArgsParser('verb-macro'))],
            environments=[EnvironmentSpec('minipage', args_parser='{'), EnvironmentSpec('minted', args_parser='{')]
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
