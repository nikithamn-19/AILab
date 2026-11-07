
import re
from itertools import product

# Tokenize the logical expression
def tokenize(expression):
    pattern = r'<->|->|[()&|~!]|[A-Za-z][A-Za-z0-9_]*'
    tokens = re.findall(pattern, expression)

    if ''.join(tokens) != re.sub(r'\s+', '', expression):
        raise ValueError("Invalid character in expression")

    return tokens


# Recursive descent parser
class Parser:
    def __init__(self, expression):
        self.tokens = tokenize(expression)
        self.pos = 0

    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def match(self, *values):
        if self.current() in values:
            self.pos += 1
            return True
        return False

    def parse_iff(self):
        node = self.parse_imp()

        while self.match('<->', 'IFF', 'iff'):
            node = ('iff', node, self.parse_imp())

        return node

    def parse_imp(self):
        node = self.parse_or()

        if self.match('->', 'IMPLIES', 'implies'):
            node = ('imp', node, self.parse_imp())

        return node

    def parse_or(self):
        node = self.parse_and()

        while self.match('|', 'OR', 'or'):
            node = ('or', node, self.parse_and())

        return node

    def parse_and(self):
        node = self.parse_not()

        while self.match('&', 'AND', 'and'):
            node = ('and', node, self.parse_not())

        return node

    def parse_not(self):
        if self.match('~', '!', 'NOT', 'not'):
            return ('not', self.parse_not())

        return self.parse_atom()

    def parse_atom(self):
        token = self.current()

        if token is None:
            raise ValueError("Unexpected end of expression")

        if self.match('('):
            node = self.parse_iff()

            if not self.match(')'):
                raise ValueError("Missing closing parenthesis")

            return node

        if re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*', token):
            self.pos += 1

            if token.lower() in ('and', 'or', 'not',
                                  'implies', 'iff'):
                raise ValueError("Unexpected operator: " + token)

            return ('symbol', token)

        raise ValueError("Unexpected token: " + token)

    def parse(self):
        node = self.parse_iff()

        if self.current() is not None:
            raise ValueError("Unexpected token: " + self.current())

        return node


# Evaluate a logical expression
def evaluate(node, model):
    op = node[0]

    if op == 'symbol':
        return model[node[1]]

    if op == 'not':
        return not evaluate(node[1], model)

    left = evaluate(node[1], model)
    right = evaluate(node[2], model)

    if op == 'and':
        return left and right

    if op == 'or':
        return left or right

    if op == 'imp':
        return (not left) or right

    if op == 'iff':
        return left == right


# Find all symbols
def get_symbols(node):
    if node[0] == 'symbol':
        return {node[1]}

    if node[0] == 'not':
        return get_symbols(node[1])

    return get_symbols(node[1]) | get_symbols(node[2])


# Display truth table
def print_truth_table(kb, alpha, symbols):

    print("\nTRUTH TABLE")
    print("-" * 55)

    headers = symbols + ["KB", "Alpha"]

    print(" | ".join(f"{h:^8}" for h in headers))
    print("-" * 55)

    for values in product([True, False], repeat=len(symbols)):

        model = dict(zip(symbols, values))

        kb_result = evaluate(kb, model)
        alpha_result = evaluate(alpha, model)

        row = list(values) + [kb_result, alpha_result]

        print(" | ".join(
            f"{'T' if v else 'F':^8}" for v in row
        ))

    print("-" * 55)


# TT-CHECK-ALL algorithm
def tt_check_all(kb, alpha, symbols, model):

    if not symbols:
        if evaluate(kb, model):
            return evaluate(alpha, model)
        else:
            return True

    P = symbols[0]
    rest = symbols[1:]

    # Check P = True
    model_true = model.copy()
    model_true[P] = True

    result_true = tt_check_all(
        kb, alpha, rest, model_true
    )

    # Check P = False
    model_false = model.copy()
    model_false[P] = False

    result_false = tt_check_all(
        kb, alpha, rest, model_false
    )

    return result_true and result_false


# TT-ENTAILS algorithm
def tt_entails(kb_expression, alpha_expression):

    kb = Parser(kb_expression).parse()
    alpha = Parser(alpha_expression).parse()

    symbols = sorted(
        get_symbols(kb) | get_symbols(alpha)
    )

    # Print truth table
    print_truth_table(kb, alpha, symbols)

    # Check entailment
    return tt_check_all(kb, alpha, symbols, {})


# Main program
try:
    print("TRUTH TABLE ENTAILMENT")
    print("======================")

    kb_input = input("Enter Knowledge Base (KB): ")
    alpha_input = input("Enter Query (alpha): ")

    result = tt_entails(kb_input, alpha_input)

    print("\nFINAL RESULT")
    print("============")

    if result:
        print("TRUE: KB entails alpha.")
    else:
        print("FALSE: KB does not entail alpha.")

except ValueError as e:
    print("Invalid expression:", e)
