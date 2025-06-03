import ast
import operator


class Evaluator:
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

    @staticmethod
    def eval(expr: str) -> bool:
        """
        Safely evaluates a boolean expression string using a limited subset of Python's AST.
        Only logical and comparison operations are allowed.
        """

        def _eval(node):
            if isinstance(node, ast.Expression):
                return _eval(node.body)
            elif isinstance(node, ast.BoolOp):
                values = [_eval(v) for v in node.values]
                return Evaluator.ALLOWED_OPERATORS[type(node.op)](values[0], values[1]) if len(values) > 1 else values[0]
            elif isinstance(node, ast.Compare):
                left = _eval(node.left)
                for op, comp in zip(node.ops, node.comparators):
                    right = _eval(comp)
                    if not Evaluator.ALLOWED_OPERATORS[type(op)](left, right):
                        return False
                    left = right
                return True
            elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
                return not _eval(node.operand)
            elif isinstance(node, ast.Constant):
                return node.value
            else:
                raise ValueError(f"Unsupported expression: {ast.dump(node)}")

        try:
            tree = ast.parse(expr, mode='eval')
            return _eval(tree)
        except Exception as e:
            raise ValueError(f"Failed to evaluate expression '{expr}': {e}")
