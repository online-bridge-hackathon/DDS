# Check compatibility
try:
    name = "Monty"
    eval("f\"Hello, {name}\"")
except SyntaxError:
    raise RuntimeError(
        "DDS requires f-string support, introduced in Python 3.6")
