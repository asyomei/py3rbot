start = "Hi! I'm Python Bot. Usage: /help"

help = """\
Usage:
  - Reply to me python code
  - /py command (help: /py)
  - via me (help: /inline)
Python version: {python_version}
"""

py_cmd_help = """\
Usage:
  /py [/<args>] <code>
Example:
  /py print("Hi!")
Argmunets:
  e - Eval mode (help: /eval)
"""

inline_help = """\
Usage:
  @{botname} [/<args>] <code>
Example:
  @{botname} print(6 * 7)
Arguments:
  e - Eval mode (help: /eval)
  r - Remove code from result message
"""

eval_help = """\
Eval mode as print(eval(...))
Default imported math, random modules
Example:
  /e math.sqrt(4 + 5) # output: 3.0
"""

empty = "empty"
too_long_output = "too long output"
was_terminated = "execution time exceeded"

output = "Output"
run_code = "Run code"
running = "Running..."
