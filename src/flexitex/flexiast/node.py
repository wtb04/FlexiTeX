from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Literal
import re


@dataclass
class Arg:
    type: str
    value: str


@dataclass
class ASTNode:
    type: Literal["macro", "environment", "root", "text", "comment"]
    name: str
    args: List[Arg] = field(default_factory=list)
    text: str = ""
    children: List[ASTNode] = field(default_factory=list)
    parent: Optional[ASTNode] = None
    _file_name: str = ""

    def add_child(self, child: ASTNode):
        child.parent = self
        self.children.append(child)

    @property
    def is_root(self): return self.type == "root"
    @property
    def is_env(self): return self.type == "environment"
    @property
    def is_macro(self): return self.type == "macro"
    @property
    def is_text(self): return self.type == "text"
    @property
    def is_comment(self): return self.type == "comment"
    @property
    def _splitted(self): return bool(self._file_name)

    def arg(self, n: int) -> str:
        if n < len(self.args):
            return self.args[n].value
        return ""

    def has_next_sibling_of_type(self, t: Literal["macro", "environment", "root", "text", "comment"]) -> bool:
        if self.parent is None:
            return False
        siblings = self.parent.children
        try:
            idx = siblings.index(self)
        except ValueError:
            return False
        if idx + 1 < len(siblings):
            return siblings[idx + 1].type == t
        return False

    def find_closest(self, type: Literal["macro", "environment", "text", "comment"], name: str):
        current = self
        while current is not None and not current.is_root:
            if current.name == name and current.type == type:
                return current
            current = current.parent
        return None

    def index(self, parent_name=None) -> int:
        if self.is_root:
            return -1
        if parent_name is None or parent_name == self.name:
            siblings = [
                c for c in self.parent.children
                if c.type == self.type and c.name == self.name
            ]
            for idx, s in enumerate(siblings):
                if s is self:
                    return idx + 1
        return self.parent.index(parent_name)

    @property
    def length(self) -> int:
        base = 2 if self.is_env else 1 if self.is_macro else 0
        base += max(self.text.count('\n'), 1) if self.text else 0
        return base + sum(c.length for c in self.children if not c._splitted)

    @property
    def width(self) -> int:
        width = max(len(line)
                    for line in self.text.splitlines()) if self.is_text else 0
        return max(width, *(c.width for c in self.children if not c._splitted))

    def __str__(self) -> str:
        lines = []

        def walk(node: ASTNode, depth: int = 0):
            indent = "  " * depth
            line = f"{indent}- {node.type}: {node.name} ({node._format_args()}) - {node.length} line(s)"
            if node.text:
                summary = re.sub(r'\s+', ' ', node.text).strip()
                if summary:
                    line += f" — {summary[:30]}…" if len(
                        summary) > 30 else f" — {summary}"
            lines.append(line)
            for child in node.children:
                walk(child, depth + 1)
        walk(self)
        return "\n".join(lines)

    def _format_args(self) -> str:
        return ", ".join(f"{a.type}={a.value}" for a in self.args)
