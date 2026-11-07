
import re

# Check whether a term is a variable
# Convention: lowercase names are variables
def is_variable(term):
    return term[0] == 'var'


# Apply existing substitutions to a term
def apply_subst(term, subst):
    if is_variable(term):
        name = term[1]

        if name in subst:
            return apply_subst(subst[name], subst)

        return term

    if term[0] in ('const',):
        return term

    if term[0] in ('func', 'pred'):
        return (term[0], term[1],
                tuple(apply_subst(x, subst) for x in term[2]))

    return term


# Occurs check
def occurs(variable, term, subst):
    term = apply_subst(term, subst)

    if is_variable(term):
        return variable == term[1]

    if term[0] in ('func', 'pred'):
        return any(occurs(variable, x, subst)
                   for x in term[2])

    return False


# Tokenize input
def tokenize(expression):
    tokens = re.findall(
        r'[A-Za-z][A-Za-z0-9_]*|[(),]',
        expression
    )

    if ''.join(tokens) != re.sub(r'\s+', '', expression):
        raise ValueError("Invalid expression")

    return tokens


# Parser for predicates and terms
class Parser:

    def __init__(self, expression):
        self.tokens = tokenize(expression)
        self.pos = 0

    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def match(self, value):
        if self.current() == value:
            self.pos += 1
            return True
        return False

    def parse_term(self):

        name = self.current()

        if name is None:
            raise ValueError("Unexpected end of input")

        self.pos += 1

        # Function with arguments
        if self.match('('):
            args = [self.parse_term()]

            while self.match(','):
                args.append(self.parse_term())

            if not self.match(')'):
                raise ValueError("Missing closing parenthesis")

            return ('func', name, tuple(args))

        # Lowercase = variable
        if name[0].islower():
            return ('var', name)

        # Uppercase = constant
        return ('const', name)

    def parse(self):

        name = self.current()

        if name is None or not name[0].isupper():
            raise ValueError(
                "Predicate name must start with uppercase"
            )

        self.pos += 1

        if not self.match('('):
            raise ValueError("Expected '(' after predicate")

        args = [self.parse_term()]

        while self.match(','):
            args.append(self.parse_term())

        if not self.match(')'):
            raise ValueError("Missing closing parenthesis")

        if self.current() is not None:
            raise ValueError("Unexpected extra input")

        return ('pred', name, tuple(args))


# Unification algorithm
def unify(x, y, subst=None):

    if subst is None:
        subst = {}

    x = apply_subst(x, subst)
    y = apply_subst(y, subst)

    # Step 1: If both are identical, return NIL
    if x == y:
        return subst

    # Step 1: First term is a variable
    if is_variable(x):

        if occurs(x[1], y, subst):
            return None

        subst[x[1]] = y
        return subst

    # Step 1: Second term is a variable
    if is_variable(y):

        if occurs(y[1], x, subst):
            return None

        subst[y[1]] = x
        return subst

    # Step 2: Check predicate/function/constant types
    if x[0] != y[0]:
        return None

    # Constants must be identical
    if x[0] == 'const':
        return None

    # Step 2: Check names
    if x[1] != y[1]:
        return None

    # Step 3: Check number of arguments
    if len(x[2]) != len(y[2]):
        return None

    # Step 4 and 5: Initialize and compare arguments
    for a, b in zip(x[2], y[2]):

        subst = unify(a, b, subst)

        # Step 5(b): Check failure
        if subst is None:
            return None

    # Step 6: Return substitution set
    return subst


# Display substitutions
def display_substitution(subst):

    if not subst:
        print("NIL (No substitution required)")
        return

    print("Substitution set:")

    for variable, value in subst.items():
        value = apply_subst(value, subst)
        print(variable, "=", format_term(value))


# Convert parsed terms into readable expressions
def format_term(term):

    if term[0] in ('var', 'const'):
        return term[1]

    if term[0] in ('func', 'pred'):
        args = ", ".join(format_term(x) for x in term[2])
        return term[1] + "(" + args + ")"

    return str(term)


# Main program: User input
try:

    print("UNIFICATION ALGORITHM")
    print("=====================")

    expr1 = input("Enter first expression: ")
    expr2 = input("Enter second expression: ")

    # Parse expressions
    p1 = Parser(expr1).parse()
    p2 = Parser(expr2).parse()

    # Step 1: Unify both expressions
    result = unify(p1, p2)

    print("\nFINAL RESULT")
    print("============")

    if result is None:
        print("FAILURE: Expressions cannot be unified.")

    elif not result:
        print("NIL: No substitution required.")

    else:
        print("SUCCESS: Expressions can be unified.")
        display_substitution(result)

        print("\nUnified Expression 1:")
        print(format_term(apply_subst(p1, result)))

        print("Unified Expression 2:")
        print(format_term(apply_subst(p2, result)))

except ValueError as e:
    print("Invalid input:", e)
