import re
from pylatexenc.latexwalker import (
    LatexCharsNode, LatexMacroNode, LatexEnvironmentNode, LatexGroupNode, LatexCommentNode
)
from flexitex.flexiast.node import ASTNode, Arg
from typing import List


STRUCTURAL_MACROS = {
    "part": -1,
    "chapter": 0,
    "section": 1,
    "subsection": 2,
    "subsubsection": 3,
    "paragraph": 4,
    "subparagraph": 5,
}


def is_structural_macro(name: str) -> bool:
    return name in STRUCTURAL_MACROS


def structural_level(name: str) -> int:
    return STRUCTURAL_MACROS.get(name, float('inf'))


def parse_arguments(parsed_args) -> List[Arg]:
    args = []
    for arg in parsed_args.argnlist:
        if arg is None:
            continue
        if isinstance(arg, LatexGroupNode):
            value = ''.join(
                n.chars if isinstance(n, LatexCharsNode) else
                n.latex_verbatim() if isinstance(n, LatexMacroNode) else
                ''
                for n in arg.nodelist
            ).strip()
            delimiter = ''.join(arg.delimiters)
            args.append(Arg(type=delimiter, value=value))
        elif isinstance(arg, LatexMacroNode):
            args.append(Arg(type='macro', value=arg.latex_verbatim()))
    return args


def to_ast(node_list, latex_source: str) -> ASTNode:
    root = ASTNode("root", "root")
    stack = [root]

    for node in node_list:
        if isinstance(node, LatexEnvironmentNode):
            env_node = ASTNode(
                "environment", node.environmentname,
                args=parse_arguments(node.nodeargd)
            )
            stack[-1].add_child(env_node)
            
            # Special handling for verbatim
            if hasattr(node.nodeargd, 'verbatim_text') and node.nodeargd.verbatim_text:
                env_node.add_child(ASTNode("text", "text", text=node.nodeargd.verbatim_text.strip()))

            # Recurse into environment content
            children_ast = to_ast(node.nodelist, latex_source)
            for child in children_ast.children:
                env_node.add_child(child)

        elif isinstance(node, LatexMacroNode):
            macro_name = node.macroname
            macro_node = ASTNode(
                "macro", macro_name,
                args=parse_arguments(node.nodeargd)
            )

            if is_structural_macro(macro_name):
                level = structural_level(macro_name)

                # Pop stack until we find a suitable parent
                while len(stack) > 1:
                    top = stack[-1]
                    if top.type == "macro" and is_structural_macro(top.name):
                        if structural_level(top.name) < level:
                            break
                    elif top.type == "environment":
                        break
                    stack.pop()

                stack[-1].add_child(macro_node)
                stack.append(macro_node)
            else:
                stack[-1].add_child(macro_node)

        elif isinstance(node, LatexCharsNode):
            text_content = re.sub(r'\n{3,}', '\n\n', node.chars)
            if text_content:
                text_node = ASTNode("text", "text", text=text_content)
                stack[-1].add_child(text_node)

        elif isinstance(node, LatexGroupNode):
            # Groups are usually arguments, but if standalone in the flow, treat as flat
            group_text = ''.join(
                n.chars if isinstance(n, LatexCharsNode) else
                n.latex_verbatim() if isinstance(n, LatexMacroNode) else ''
                for n in node.nodelist
            ).strip()
            if group_text:
                text_node = ASTNode("text", "text", text=group_text)
                stack[-1].add_child(text_node)

        elif isinstance(node, LatexCommentNode):
            comment_text = node.comment
            if comment_text:
                comment_node = ASTNode("comment", "comment", text=comment_text)
                stack[-1].add_child(comment_node)

    return root
