from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List, Literal

import re
import ast
import operator

from flexitex.flexiast.builder import STRUCTURAL_MACROS
from flexitex.flexiast.node import ASTNode
from flexitex.flexiast.evaluator import Evaluator


@dataclass
class NodeRule:
    type: Literal["macro", "environment", "text"]
    name: str
    file_name: str
    condition: Optional[str] = None

    ALLOWED_OPERATORS = {
        ast.Eq: operator.eq,
        ast.NotEq: operator.ne,
        ast.Lt: operator.lt,
        ast.LtE: operator.le,
        ast.Gt: operator.gt,
        ast.GtE: operator.ge,
        ast.And: lambda a, b: a and b,
        ast.Or: lambda a, b: a or b,
        ast.Not: operator.not_,
    }

    def match_condition(self, node: "ASTNode") -> bool:
        if not self.condition:
            return True

        real_condition = Structure.substitute_placeholders(
            self.condition, node)
        return Evaluator.eval(real_condition)


@dataclass
class Structure:
    output_path: str
    output_main_file: str
    rules: List[NodeRule]

    @staticmethod
    def substitute_placeholders(text: str, node: "ASTNode"):
        def normalize_name(name: str):
            name = name.lower()
            # Replace all characters except a-z, 0-9, hyphen and underscore with underscore
            name = re.sub(r'[^a-z0-9\-_]+', '_', name)
            # Collapse multiple underscores into one
            name = re.sub(r'_+', '_', name)
            # Strip leading/trailing underscores
            name = name.strip('_')
            return name

        def replace_brackets(match):
            key = match.group(1)
            # Replace with structural macros name
            if key.startswith("name:"):
                macro_name = key[5:]

                if macro_name not in STRUCTURAL_MACROS:
                    raise ValueError(
                        f"[name:{macro_name}] is not a valid structural macro")

                target_node = node.find_closest('macro', macro_name)
                if target_node is None:
                    return f"[name:{macro_name}]"

                return normalize_name(target_node.arg(0))

            idx = node.index(key)
            return str(idx) if idx != -1 else f"[{key}]"

        def replace_angles(match):
            attr = match.group(1)
            val = getattr(node, attr, None)
            return str(val) if val is not None else f"<{attr}>"

        text = re.sub(r"\[([\w:-]+)\]", replace_brackets, text)
        text = re.sub(r"<(\w+)>", replace_angles, text)

        return text

    def check_split(self, node: "ASTNode") -> str:
        """
        Checks if a node should be split based on the NodeRules
        """
        # List of all rules matching node's name and type
        applying_rules = [
            rule for rule in self.rules
            if node.name == rule.name and node.type == rule.type
        ]

        if not applying_rules:
            return ""

        for rule in applying_rules:
            if rule.match_condition(node):
                return self.substitute_placeholders(rule.file_name, node)

        return ""
