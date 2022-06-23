def _(string: str):
    string = string.strip()
    def format_str(**kwargs) -> str:
        return string.format_map(kwargs)
    return format_str


start = _("Hi! I'm Python Bot. Usage: /help")

help = _("""\
Usage:
  - Reply to me python code
  - /py command (help: /py)
  - via me (help: /inline)
Python version: {python_version}
""")

py_cmd_help = _("""\
Usage:
  /py [/<args>] <code>
Example:
  /py print("Hi!")
Argmunets:
  e - Eval mode (help: /eval)
""")

inline_help = _("""\
Usage:
  @{botname} [/<args>] <code>
Example:
  @{botname} print(6 * 7)
Arguments:
  e - Eval mode (help: /eval)
  r - Remove code from result message
""")

eval_help = _("""\
Eval mode as print(eval(...))
Default imported math, random modules
Example:
  /e math.sqrt(4 + 5) # output: 3.0
""")

empty = _("empty")
too_long_output = _("too long output")
was_terminated = _("execution time exceeded")

output = _("Output")
no_code = _("No code")
run_code = _("Run code")
running = _("Running...")
too_long_query = _("Too long query")
