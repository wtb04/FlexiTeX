from flexitex.flexiast.node import ASTNode


class DotGenerator:
    def to_dot(self, node: "ASTNode", hide_before_document: bool = False) -> str:
        lines = ["digraph AST {", "  node [fontname=Helvetica];"]

        def escape(text: str) -> str:
            return text.replace("\\", "\\\\").replace("\"", "\\\"")

        def add_node(node: "ASTNode", node_id: int = 0, counter=[0], found_document=[not hide_before_document]) -> int:
            # Skip nodes before 'document' environment if flag is set
            if hide_before_document and not found_document[0]:
                if node.is_env and node.name == "document":
                    found_document[0] = True
                else:
                    for child in node.children:
                        add_node(child, node_id, counter, found_document)
                    return node_id

            current_id = counter[0]

            if node.is_macro:
                color = "lightblue"
            elif node.is_env:
                color = "lightgreen"
            elif node.is_text:
                color = "lightgray"
            elif node.is_root:
                color = "orange"
            elif node.is_comment:
                color = "lightyellow"
            else:
                color = "white"

            label = f"{node.index()}. {node.name}"
            lines.append(
                f'  {current_id} [label="{escape(label)}", style=filled, fillcolor="{color}"];')

            # 1. Add arguments node
            if node.args:
                counter[0] += 1
                args_id = counter[0]
                arg_text = "\\n".join(
                    f"{escape(arg.type)}={escape(arg.value)}" for arg in node.args)

                lines.append(
                    f'  {args_id} [label="{arg_text}", shape=box, style=dashed];')
                lines.append(f'  {current_id} -> {args_id};')
                lines.append(
                    "  { rank=same; " + f"{current_id}; {args_id}; }}")

            # 2. Add child AST nodes
            for child in node.children:
                counter[0] += 1
                child_id = counter[0]
                lines.append(f"  {current_id} -> {child_id};")
                add_node(child, child_id, counter)

            return current_id

        add_node(node)
        lines.append("}")
        return "\n".join(lines)
