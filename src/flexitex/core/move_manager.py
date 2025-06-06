import os
import copy
import shutil
from typing import List, Tuple, Dict, Set
from flexitex.flexiast.node import ASTNode


class MoveManager:
    def __init__(self, base_dir: str, base_output_dir: str, fig_dir: str):
        self.base_dir = base_dir
        self.base_output_dir = base_output_dir
        self.fig_dir = fig_dir
        self._graphics_moves: List[Tuple[str, str]] = []
        self._static_moves: List[Tuple[str, str]] = []
        self._excluded_exts = ['.tex', '.log', '.aux',
                               '.fls', '.fdb_latexmk', '.out', '.toc', '.gz']

    @property
    def _moves(self) -> List[Tuple[str, str]]:
        return self._graphics_moves + self._static_moves

    def detect_moves(self, ast: ASTNode) -> ASTNode:
        new_ast = self.detect_graphics_moves(ast)
        self.detect_static_files()
        return new_ast

    def detect_graphics_moves(self, ast: ASTNode) -> ASTNode:
        """
        Detects all includegraphics macros, updates their paths in a deep-copied AST,
        and stores the (src, dst) moves for later use.
        Returns the new AST.
        """
        graphics_paths: List[str] = []

        def walk(node: ASTNode):
            if node.is_macro and node.name == "includegraphics" and node.args:
                # Use the last argument with braces as the path
                for arg in reversed(node.args):
                    if arg.type == '{}':
                        graphics_paths.append(arg.value)
                        break
            for child in node.children:
                walk(child)
        walk(ast)

        # Deduplicate and assign output names
        used_names: Set[str] = set()
        src_to_dst: Dict[str, str] = {}
        for src_path in graphics_paths:
            if src_path not in src_to_dst:
                base_name = os.path.basename(src_path)
                name, ext = os.path.splitext(base_name)
                candidate = base_name
                i = 1
                while os.path.join(self.fig_dir, candidate) in used_names:
                    candidate = f"{name}{i}{ext}"
                    i += 1
                rel_dst = os.path.join(self.fig_dir, candidate)
                used_names.add(rel_dst)
                src_to_dst[src_path] = rel_dst

        # Deep copy AST and update image paths
        new_ast = copy.deepcopy(ast)

        def update_paths(node: ASTNode):
            if node.is_macro and node.name == "includegraphics" and node.args:
                for arg in reversed(node.args):
                    if arg.type == '{}' and arg.value in src_to_dst:
                        arg.value = src_to_dst[arg.value]
                        break
            for child in node.children:
                update_paths(child)
        update_paths(new_ast)

        self._graphics_moves = [
            (os.path.join(self.base_dir, src),
             os.path.join(self.base_output_dir, rel_dst))
            for src, rel_dst in src_to_dst.items()
        ]

        return new_ast

    def detect_static_files(self):
        already_moved_srcs = set(os.path.abspath(src)
                                 for src, _ in self._graphics_moves)

        for root, _, files in os.walk(self.base_dir):
            for filename in files:
                full_src = os.path.join(root, filename)
                if os.path.splitext(full_src)[1] in self._excluded_exts:
                    continue
                if os.path.abspath(full_src) in already_moved_srcs:
                    continue

                rel_path = os.path.relpath(full_src, self.base_dir)
                dst_path = os.path.join(self.base_output_dir, rel_path)
                self._static_moves.append((full_src, dst_path))

    def move_files(self):
        """
        Copies all detected images to their new locations.
        """
        for src, dst in self._moves:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
