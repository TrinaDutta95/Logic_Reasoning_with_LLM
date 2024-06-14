import re


def fix_missing_parentheses(expression):
    """
    Fix missing parentheses in the given FOL expression.

    Parameters:
    expression (str): The FOL expression to fix.

    Returns:
    str: The fixed FOL expression with balanced parentheses.
    """
    # Count the number of opening and closing parentheses
    opening_count = expression.count('(')
    closing_count = expression.count(')')
    diff = opening_count - closing_count

    # Add missing closing parentheses
    if diff > 0:
        expression += ')' * diff

    # Add missing opening parentheses
    elif diff < 0:
        # Find the position of the first closing parenthesis
        index = expression.find(')')
        if index != -1:
            # Count the number of opening and closing parentheses before the first closing parenthesis
            opening_before = expression[:index].count('(')
            closing_before = opening_before
            # Find the matching opening parenthesis
            while closing_before > 0 and index >= 0:
                index -= 1
                if expression[index] == ')':
                    closing_before += 1
                elif expression[index] == '(':
                    opening_before += 1
            # Add missing opening parentheses before the first closing parenthesis
            expression = expression[:index] + '(' * (closing_before - opening_before) + expression[index:]

    return expression


def validate_fol_expression(expression):
    """
    Validate the given FOL expression for syntax correctness, consistency, and balanced parentheses.

    Parameters:
    expression (str): The FOL expression to validate.

    Returns:
    str: The fixed FOL expression with balanced parentheses.
    """
    # Fix missing parentheses
    expression = fix_missing_parentheses(expression)

    # Check for balanced parentheses
    def check_parentheses_balance(expr):
        stack = []
        for char in expr:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    return False
                stack.pop()
        return not stack

    if not check_parentheses_balance(expression):
        return None

    # Simple regex to check for common FOL syntax issues
    fol_syntax_pattern = r'^[\w\s\(\)\&\|\~\->,]+$'
    if not re.match(fol_syntax_pattern, expression):
        return None

    # Check for consistent use of symbols as predicates or functions
    symbols = re.findall(r'\b\w+\b', expression)
    symbol_types = {}
    for symbol in symbols:
        if '(' in expression.split(symbol)[1]:
            if symbol in symbol_types and symbol_types[symbol] != 'predicate':
                return None
            symbol_types[symbol] = 'predicate'
        else:
            if symbol in symbol_types and symbol_types[symbol] != 'variable':
                return None
            symbol_types[symbol] = 'variable'

    return expression


def validate_fol_statements(fol_statements):
    """
    Validate a list of FOL statements.

    Parameters:
    fol_statements (list): List of FOL statements to validate.

    Returns:
    bool: True if all statements are valid, False otherwise.
    """
    for i, statement in enumerate(fol_statements):
        fixed_statement = validate_fol_expression(statement)
        if fixed_statement is None:
            print(f"Statement {i + 1} has syntax or consistency issues and could not be fixed.")
            return False
        fol_statements[i] = fixed_statement
    return True
