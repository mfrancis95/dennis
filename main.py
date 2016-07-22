tokens = (
    "ASSIGN",
    "IF",
    "THEN",
    "ELSE",
    "NOT",
    "AND",
    "OR",
    "NULL",
    "STRING",
    "NUMBER",
    "IDENTIFIER",
    "EQUALS",
    "LEFTARROW",
    "RIGHTARROW",
    "SEMICOLON",
    "ARROW",
    "LEFTPAREN",
    "RIGHTPAREN",
    "LEFTBRACK",
    "RIGHTBRACK",
    "COMMA",
    "NOTEQUAL",
    "LESSTHAN",
    "LESSTHANEQ",
    "GREATERTHAN",
    "GREATERTHANEQ",
    "MULTIPLY",
    "DIVIDE",
    "MOD",
    "PLUS",
    "MINUS"
)

def t_IF(t):
    "if"
    return t

def t_THEN(t):
    "then"
    return t

def t_ELSE(t):
    "else"
    return t

def t_NOT(t):
    "not"
    return t

def t_AND(t):
    "and"
    return t

def t_OR(t):
    "or"
    return t

def t_NULL(t):
    "null"
    t.value = None
    return t

def t_STRING(t):
    r"\"[^\"]*\""
    t.value = t.value[1:-1]
    return t

def t_NUMBER(t):
    r"-?\d*\.?\d+"
    t.value = (float if "." in t.value else int)(t.value)
    return t

def t_IDENTIFIER(t):
    r"[A-Za-z][A-Za-z0-9_]*"
    return t

t_ASSIGN = "="
t_SEMICOLON = ";"
t_ARROW = "->"
t_LEFTPAREN = r"\("
t_RIGHTPAREN = r"\)"
t_LEFTBRACK = r"\["
t_RIGHTBRACK = r"\]"
t_COMMA = ","
t_EQUALS = "=="
t_NOTEQUAL = "!="
t_LESSTHAN = "<"
t_LESSTHANEQ = "<="
t_GREATERTHAN = ">"
t_GREATERTHANEQ = ">="
t_MULTIPLY = r"\*"
t_DIVIDE = "/"
t_MOD = "%"
t_PLUS = r"\+"
t_MINUS = "-"

t_ignore = " \t"

def t_error(t):
    t.lexer.skip(1)

from ply import lex
lexer = lex.lex()

precedence = (
    ("left", "OR"),
    ("left", "AND"),
    ("left", "NOT"),
    ("left", "EQUALS", "NOTEQUAL", "LESSTHAN", "LESSTHANEQ", "GREATERTHAN", "GREATERTHANEQ"),
    ("left", "PLUS", "MINUS"),
    ("left", "MULTIPLY", "DIVIDE", "MOD"),
    ("left", "LEFTPAREN")
)

def p_statements_one(p):
    "statements : statement"
    p[0] = ("statements", [p[1]])

def p_statements_many(p):
    "statements : statement statements"
    p[0] = ("statements", [p[1]] + [p[2]])

def p_statement_assign(p):
    "statement : IDENTIFIER ASSIGN expression SEMICOLON"
    p[0] = ("assign", p[1], p[3])

def p_statement_expression(p):
    "statement : expression SEMICOLON"
    p[0] = p[1]

def p_expression_function_define_none(p):
    "expression : LEFTPAREN RIGHTPAREN ARROW expression"
    p[0] = ("function-define", [], p[4])

def p_expression_function_define_one(p):
    "expression : LEFTPAREN IDENTIFIER RIGHTPAREN ARROW expression"
    p[0] = ("function-define", [p[2]], p[5])

def p_expression_function_define_many(p):
    "expression : LEFTPAREN IDENTIFIER identifiers RIGHTPAREN ARROW expression"
    p[0] = ("function-define", [p[2]] + p[3], p[6])

def p_identifiers_one(p):
    "identifiers : COMMA IDENTIFIER"
    p[0] = [p[2]]

def p_identifiers_many(p):
    "identifiers : COMMA IDENTIFIER identifiers"
    p[0] = [p[2]] + p[3]

def p_expression_function_call_none(p):
    "expression : expression LEFTPAREN RIGHTPAREN"
    p[0] = ("function-call", p[1], [])

def p_expression_function_call_one(p):
    "expression : expression LEFTPAREN expression RIGHTPAREN"
    p[0] = ("function-call", p[1], [p[3]])

def p_expression_function_call_many(p):
    "expression : expression LEFTPAREN expression expressions RIGHTPAREN"
    p[0] = ("function-call", p[1], [p[3]] + p[4])

def p_expressions_one(p):
    "expressions : COMMA expression"
    p[0] = [p[2]]

def p_expressions_many(p):
    "expressions : COMMA expression expressions"
    p[0] = [p[2]] + p[3]

def p_expression_if(p):
    "expression : IF expression THEN expression ELSE expression"
    p[0] = ("if", p[2], p[4], [], p[6])

def p_expression_if_else_if(p):
    "expression : IF expression THEN expression else_ifs ELSE expression"
    p[0] = ("if", p[2], p[4], p[5], p[7])

def p_else_ifs_one(p):
    "else_ifs : ELSE IF expression THEN expression"
    p[0] = [("else-if", p[3], p[5])]

def p_else_ifs_many(p):
    "else_ifs : ELSE IF expression THEN expression else_ifs"
    p[0] = [("else-if", p[3], p[5])] + p[6]

def p_expression_multiply(p):
    "expression : expression MULTIPLY expression"
    p[0] = ("multiply", p[1], p[3])

def p_expression_divide(p):
    "expression : expression DIVIDE expression"
    p[0] = ("divide", p[1], p[3])

def p_expression_mod(p):
    "expression : expression MOD expression"
    p[0] = ("mod", p[1], p[3])

def p_expression_plus(p):
    "expression : expression PLUS expression"
    p[0] = ("plus", p[1], p[3])

def p_expression_minus(p):
    "expression : expression MINUS expression"
    p[0] = ("minus", p[1], p[3])

def p_expression_equals(p):
    "expression : expression EQUALS expression"
    p[0] = ("equals", p[1], p[3])

def p_expression_notequal(p):
    "expression : expression NOTEQUAL expression"
    p[0] = ("notequal", p[1], p[3])

def p_expression_lessthan(p):
    "expression : expression LESSTHAN expression"
    p[0] = ("lessthan", p[1], p[3])

def p_expression_lessthanorequal(p):
    "expression : expression LESSTHANEQ expression"
    p[0] = ("lessthanorequal", p[1], p[3])

def p_expression_greaterthan(p):
    "expression : expression GREATERTHAN expression"
    p[0] = ("greaterthan", p[1], p[3])

def p_expression_greaterthanorequal(p):
    "expression : expression GREATERTHANEQ expression"
    p[0] = ("greaterthanorequal", p[1], p[3])

def p_expression_not(p):
    "expression : NOT expression"
    p[0] = ("not", p[2])

def p_expression_and(p):
    "expression : expression AND expression"
    p[0] = ("and", p[1], p[3])

def p_expression_or(p):
    "expression : expression OR expression"
    p[0] = ("or", p[1], p[3])

def p_expression_expression(p):
    "expression : LEFTPAREN expression RIGHTPAREN"
    p[0] = p[2]

def p_expression_list_none(p):
    "expression : LEFTBRACK RIGHTBRACK"
    p[0] = ("list", [])

def p_expression_list_one(p):
    "expression : LEFTBRACK expression RIGHTBRACK"
    p[0] = ("list", [p[2]])

def p_expression_list_many(p):
    "expression : LEFTBRACK expression expressions RIGHTBRACK"
    p[0] = ("list", [p[2]] + p[3])

def p_expression_string(p):
    "expression : STRING"
    p[0] = ("string", p[1])

def p_expression_integer(p):
    "expression : NUMBER"
    p[0] = ("number", p[1])

def p_expression_identifier(p):
    "expression : IDENTIFIER"
    p[0] = ("identifier", p[1])

def p_expression_null(p):
    "expression : NULL"
    p[0] = ("null", p[1])

def p_error(p):
    raise Exception("SYNTAX ERROR")

evaluators = {}
identifiers = {
    "head": "head",
    "float": "float",
    "int": "int",
    "print": "print",
    "tail": "tail",
    "type": "type"
}
stack = []

def evaluate(tup):
    return evaluators[tup[0]](tup)

def statement_evaluator(tup):
    for statement in tup[1]:
        evaluate(statement)

def assign_evaluator(tup):
    identifiers[tup[1]] = evaluate(tup[2])    

def function_evaluator(tup):
    if tup[0] == "function-define":
        return tup
    function = evaluate(tup[1])
    if function == "type":
        datatype = type(evaluate(tup[2][0]))
        if datatype is None:
            return "Null"
        elif datatype is tuple:
            return "Function"
        elif datatype is str:
            return "String"
        elif datatype is int:
            return "Integer"
        return datatype.__name__.capitalize()
    elif function == "print":
        result = evaluate(tup[2][0])
        if result is None:
            print("null")
        elif isinstance(result, tuple):
            print("Function (" + ", ".join(result[1]) + ") -> ?")
        else:
            print(result)
        return result
    elif function == "int":
        return int(evaluate(tup[2][0]))
    elif function == "float":
        return float(evaluate(tup[2][0]))
    elif function == "head":
        return evaluate(tup[2][0])[0]
    elif function == "tail":
        return evaluate(tup[2][0])[1:]
    stack_identifiers = {
        "self": function
    }
    i = function[1]
    identifier_index = 0
    for argument in tup[2]:
        stack_identifiers[i[identifier_index]] = evaluate(argument)
        identifier_index += 1
    stack.append(stack_identifiers)
    result = evaluate(function[2])
    stack.pop()
    return result

def conditional_evaluator(tup):
    if tup[0] == "if":
        if evaluate(tup[1]):
            return evaluate(tup[2])
        elif tup[3]:
            for elseif in tup[3]:
                result = evaluate(elseif)
                if result:
                    return result
        return evaluate(tup[4])
    return evaluate(tup[2]) if evaluate(tup[1]) else 0

def arithmetic_evaluator(tup):
    operator = tup[0]
    if operator == "multiply":
        return evaluate(tup[1]) * evaluate(tup[2])
    elif operator == "divide":
        return evaluate(tup[1]) / evaluate(tup[2])
    elif operator == "mod":
        return evaluate(tup[1]) % evaluate(tup[2])
    elif operator == "plus":
        operand1 = evaluate(tup[1])
        operand2 = evaluate(tup[2])
        if operand1 is None:
            if operand2 is None:
                operand1 = []
                operand2 = []
            else:
                operand1 = "" if isinstance(operand2, str) else []
        elif operand2 is None:
            operand2 = "" if isinstance(operand1, str) else []
        if isinstance(operand1, list) and not isinstance(operand2, list):
            return operand1 + [operand2]
        elif isinstance(operand2, list) and not isinstance(operand1, list):
            return [operand1] + operand2
        return operand1 + operand2
    return evaluate(tup[1]) - evaluate(tup[2])

def comparison_evaluator(tup):
    operator = tup[0]
    if operator == "equals":
        return 1 if evaluate(tup[1]) == evaluate(tup[2]) else 0
    elif operator == "notequal":
        return 1 if evaluate(tup[1]) != evaluate(tup[2]) else 0
    elif operator == "lessthan":
        return 1 if evaluate(tup[1]) < evaluate(tup[2]) else 0
    elif operator == "lessthanorequal":
        return 1 if evaluate(tup[1]) <= evaluate(tup[2]) else 0
    elif operator == "greaterthan":
        return 1 if evaluate(tup[1]) > evaluate(tup[2]) else 0
    return 1 if evaluate(tup[1]) >= evaluate(tup[2]) else 0

def logical_evaluator(tup):
    operator = tup[0]
    if operator == "not":
        return 1 if not evaluate(tup[1]) else 0
    elif operator == "and":
        return 1 if evaluate(tup[1]) and evaluate(tup[2]) else 0
    return 1 if evaluate(tup[1]) or evaluate(tup[2]) else 0

def list_evaluator(tup):
    return list(map(evaluate, tup[1]))

def literal_evaluator(tup):
    return tup[1]

def identifier_evaluator(tup):
    identifier = tup[1]
    if stack:
        frame = stack[-1]
        if identifier in frame:
            return frame[identifier]
    if identifier in identifiers:
        return identifiers[identifier]
    raise Exception("SEMANTIC ERROR")

evaluators["statements"] = statement_evaluator
evaluators["assign"] = assign_evaluator
evaluators["function-define"] = evaluators["function-call"] = function_evaluator
evaluators["if"] = evaluators["else-if"] = conditional_evaluator
evaluators["multiply"] = evaluators["divide"] = evaluators["mod"] = evaluators["plus"] = evaluators["minus"] = arithmetic_evaluator
evaluators["equals"] = evaluators["notequal"] = evaluators["lessthan"] = evaluators["lessthanorequal"] = evaluators["greaterthan"] = evaluators["greaterthanorequal"] = comparison_evaluator
evaluators["not"] = evaluators["and"] = evaluators["or"] = logical_evaluator
evaluators["list"] = list_evaluator
evaluators["string"] = evaluators["number"] = evaluators["null"] = literal_evaluator
evaluators["identifier"] = identifier_evaluator

import sys
from ply import yacc
parser = yacc.yacc()

with open(sys.argv[1]) as f:
    lines = ""
    for line in f:
        lines += line
    try:
        evaluate(parser.parse(lines.replace("\n", "")))
    except Exception as e:
        print(e)