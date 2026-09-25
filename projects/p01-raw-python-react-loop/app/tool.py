import ast
import operator
from typing import Any

_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def safe_calculate(expression: str) -> str:
    """
    Safely evaluates a mathematical expression string using an Abstract Syntax Tree (AST).
    Prevents arbitrary code execution by strictly limiting allowed operations to basic math.
    """

    try:

        tree = ast.parse(expression, mode='eval').body

        def _eval_node(node: ast.AST) -> Any:
            """Recursively evaluates the nodes of the syntax tree."""

            if isinstance(node, ast.Constant):
                if isinstance(node.value, (int, float)):
                    return node.value
                raise TypeError(f"Unsupported constant type: {type(node.value).__name__}. Only numbers are allowed.")

            elif isinstance(node, ast.BinOp):
                left_val = _eval_node(node.left)
                right_val = _eval_node(node.right)
                op_type = type(node.op)

                if op_type not in _ALLOWED_OPERATORS:
                    raise TypeError(f"Unsupported binary operator: {op_type.__name__}")

                return _ALLOWED_OPERATORS[op_type](left_val, right_val)

            elif isinstance(node, ast.UnaryOp):
                operand_val = _eval_node(node.operand)
                op_type = type(node.op)

                if op_type not in _ALLOWED_OPERATORS:
                    raise TypeError(f"Unsupported unary operator: {op_type.__name__}")

                return _ALLOWED_OPERATORS[op_type](operand_val)

            else:
                raise TypeError(f"Unsupported expression type: {type(node).__name__}")

        result = _eval_node(tree)

        if isinstance(result, float) and result.is_integer():
            result = int(result)

        return str(result)

    except ZeroDivisionError:
        return "Error: Division by zero is mathematically undefined."
    except SyntaxError:
        return "Error: Malformed mathematical syntax. Check your parentheses and operators."
    except Exception as e: # noqa: BLE001
        return f"Error: Invalid mathematical expression. Details: {e!s}"