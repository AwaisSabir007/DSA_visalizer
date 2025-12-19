"""
Expression conversion and evaluation algorithms
Supports infix to postfix/prefix conversion and postfix evaluation
"""
from typing import List, Tuple, Optional


def tokenize_expr(expr: str) -> List[str]:
    """
    Tokenize an expression into operators, operands, and parentheses
    
    Args:
        expr: Infix expression string
    
    Returns:
        List of tokens
    """
    toks = []
    i = 0
    while i < len(expr):
        c = expr[i]
        if c.isspace():
            i += 1
            continue
        if c.isalnum():
            j = i
            while j < len(expr) and expr[j].isalnum():
                j += 1
            toks.append(expr[i:j])
            i = j
            continue
        if c in "+-*/^()":
            toks.append(c)
            i += 1
            continue
        i += 1
    return toks


def infix_to_postfix_steps(expr: str) -> Tuple[str, List[str]]:
    """
    Convert infix expression to postfix with step-by-step explanation
    
    Args:
        expr: Infix expression string
    
    Returns:
        Tuple of (postfix_expression, list_of_steps)
    """
    prec = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    output = []
    stack = []
    steps = []
    tokens = tokenize_expr(expr)
    
    for t in tokens:
        if t.isalnum():
            output.append(t)
        elif t == '(':
            stack.append(t)
        elif t == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if stack:
                stack.pop()
        else:
            while (stack and stack[-1] != '(' and 
                   ((prec.get(stack[-1], 0) > prec.get(t, 0)) or 
                    (prec.get(stack[-1], 0) == prec.get(t, 0) and t != '^'))):
                output.append(stack.pop())
            stack.append(t)
        steps.append(f"Token: {t}\nOutput: {' '.join(output)}\nStack: {' '.join(stack)}")
    
    while stack:
        output.append(stack.pop())
        steps.append(f"Drain stack\nOutput: {' '.join(output)}\nStack: {' '.join(stack)}")
    
    return " ".join(output), steps


def infix_to_prefix_steps(expr: str) -> Tuple[str, List[str]]:
    """
    Convert infix expression to prefix with step-by-step explanation
    
    Args:
        expr: Infix expression string
    
    Returns:
        Tuple of (prefix_expression, list_of_steps)
    """
    tokens = tokenize_expr(expr)
    tokens_rev = []
    for t in reversed(tokens):
        if t == '(':
            tokens_rev.append(')')
        elif t == ')':
            tokens_rev.append('(')
        else:
            tokens_rev.append(t)
    
    postfix, steps = infix_to_postfix_steps(" ".join(tokens_rev))
    pre_tokens = list(reversed(postfix.split()))
    # Adjust steps for prefix (simplified)
    steps = [s.replace("postfix", "prefix") for s in steps]
    return " ".join(pre_tokens), steps


def eval_postfix_steps(postfix: str) -> Tuple[Optional[float], List[str]]:
    """
    Evaluate a postfix expression with step-by-step explanation
    
    Args:
        postfix: Postfix expression string
    
    Returns:
        Tuple of (result, list_of_steps)
    """
    stack = []
    steps = []
    
    for token in postfix.split():
        steps.append(f"Token: {token}\nStack: {' '.join(map(str, stack))}")
        
        if token.isdigit():
            stack.append(int(token))
        elif token.isalnum() and not token.isdigit():
            # Variable - cannot evaluate
            return None, steps
        else:
            if len(stack) < 2:
                return None, steps
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                stack.append(a / b if b != 0 else None)
            elif token == '^':
                stack.append(a ** b)
    
    return stack[-1] if stack else None, steps
