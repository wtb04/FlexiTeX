import os
from flexitex.flexiast.node import ASTNode
from flexitex.flexiast.structure import Structure


class LatexGenerator:
    def __init__(self, rules: Structure):
        self.rules = rules
        self.generated_files: list[tuple[str, str]] = []

    def to_latex(self, node: "ASTNode") -> list[tuple[str, str]]:
        if not node.is_root:
            print(node.type)
            raise ValueError("Expected root node")

        result = "".join(self._generate_latex(child)
                         for child in node.children)
        main_path = os.path.join(
            self.rules.output_path, self.rules.output_main_file)
        self.generated_files.append((main_path, result))
        return self.generated_files

    def _generate_latex(self, node: "ASTNode") -> str:
        node._file_name = self.rules.check_split(node)
        if node._splitted:
            content = self._get_latex_string(node)
            filepath = os.path.join(self.rules.output_path, node._file_name)
            self.generated_files.append((filepath, content))

            # The newline is seperate from the normal rf because the [r]
            # makes it not understand the newline anymore since it makes
            # raw output
            return rf"\input{{{node._file_name}}}" + "\n"
        else:
            return self._get_latex_string(node)

    def _get_latex_string(self, node: "ASTNode") -> str:
        if node.is_env:
            return self._get_latex_string_environment(node)
        elif node.is_macro:
            return self._get_latex_string_macro(node)
        elif node.is_text:
            return self._get_latex_string_text(node)
        elif node.is_comment:
            return self._get_latex_string_comment(node)
        else:
            return ""

    def _get_latex_string_macro(self, node: "ASTNode") -> str:
        result = f"\\{node.name}"

        if node.args:
            for arg in node.args:
                result += arg.type[0] + arg.value + arg.type[1]
        else:
            result += " " + node.macro_post_space

        for child in node.children:
            result += self._generate_latex(child)

        return result

    def _get_latex_string_environment(self, node: "ASTNode") -> str:
        result = f"\\begin{{{node.name}}}"

        if node.args:
            for arg in node.args:
                result += arg.type[0] + arg.value + arg.type[1]

        for child in node.children:
            result += self._generate_latex(child)

        result += f"\\end{{{node.name}}}"

        return result

    def _get_latex_string_text(self, node: "ASTNode") -> str:
        return node.text

    def _get_latex_string_comment(self, node: "ASTNode") -> str:
        return "%" + node.text
