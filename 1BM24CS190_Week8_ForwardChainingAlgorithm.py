# FOL Forward Chaining with User Input

def get_fact(text):
    # Convert input sentence into lowercase words
    return text.strip().lower()


# Get facts
facts = set()

n = int(input("Enter number of facts: "))

print("\nEnter facts in simple English:")
for i in range(n):
    fact = input(f"Fact {i + 1}: ")
    facts.add(get_fact(fact))


# Get rules
rules = []

m = int(input("\nEnter number of rules: "))

print("\nRule format:")
print("condition1 AND condition2 -> conclusion")

for i in range(m):
    rule = input(f"Rule {i + 1}: ").lower()

    if "->" in rule:
        condition, conclusion = rule.split("->")
        conditions = [x.strip() for x in condition.split("and")]
        rules.append((conditions, conclusion.strip()))
    else:
        print("Invalid rule format!")


# Get query
query = input("\nEnter the query to prove: ").strip().lower()


# Forward Chaining
print("\n--- Forward Chaining Process ---")

changed = True

while changed:
    changed = False

    for conditions, conclusion in rules:

        # Check whether all conditions are available
        if all(condition in facts for condition in conditions):

            if conclusion not in facts:
                facts.add(conclusion)
                print("Derived:", conclusion)
                changed = True


# Check query
print("\n--- Result ---")

if query in facts:
    print("Success - Query PROVED:", query)
else:
    print("Failure - Query:", query," is not TRUE")