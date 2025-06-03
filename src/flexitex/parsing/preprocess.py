import os
from dataclasses import dataclass
from pylatexenc.latexwalker import LatexMacroNode, LatexNode

from flexitex.parsing.parser import LatexParser


@dataclass
class PreProcess:
    @staticmethod
    def pre_process(input_folder: str, input_main_file: str) -> str:
        filepath = os.path.join(input_folder, input_main_file)
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()

        root_dir = os.path.dirname(os.path.abspath(filepath))
        expanded = PreProcess.expand_inputs(source, root_dir)
        return expanded

    @staticmethod
    def expand_inputs(source: str, root_dir: str) -> str:
        nodes = LatexParser.get_nodes_from_string(source)
        replacements = []

        def walk(node: LatexNode):
            if isinstance(node, LatexMacroNode) and node.macroname in ('input', 'include'):
                if not node.nodeargs or len(node.nodeargs) == 0:
                    return

                arg_node = node.nodeargs[0]
                if hasattr(arg_node, 'nodelist') and arg_node.nodelist:
                    filename = ''.join(
                        n.chars for n in arg_node.nodelist if hasattr(n, 'chars')).strip()
                else:
                    return

                if not filename.endswith('.tex'):
                    filename += '.tex'
                full_path = os.path.abspath(os.path.join(root_dir, filename))

                if not os.path.isfile(full_path):
                    raise ValueError(f"File not found: {filename}")
                else:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    replacement = PreProcess.expand_inputs(content, root_dir)

                replacements.append(
                    (node.pos, node.pos + node.len, replacement))

            for field in node._fields:
                child = getattr(node, field)
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, LatexNode):
                            walk(item)
                elif isinstance(child, LatexNode):
                    walk(child)

        for node in nodes:
            walk(node)

        if not replacements:
            return source

        # Replace spans in order, taking care to maintain positions
        replacements.sort()
        result = []
        last_index = 0
        for start, end, replacement in replacements:
            result.append(source[last_index:start])
            result.append(replacement)
            last_index = end
        result.append(source[last_index:])

        return ''.join(result)
