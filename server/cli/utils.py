"""Cli specific utils."""

def beautify_iter(d: dict | list, indent:int=4, base_indent:int=0):
    """colorful dictionary"""
    def colored_type(val):
        if type(val) is bool:
            return "✅" if val else "❌"
        elif isinstance(val, int):
            return '\33[33m' + str(val)
        elif isinstance(val, float):
            return '\33[94m' + str(val)
        elif isinstance(val, str):
            return '\33[32m' + val
        elif isinstance(val, bytes):
            return '\33[31m' + str(val, encoding='utf8')
        return '\33[34m' + val

    ti = indent + base_indent
    if type(d) is dict:
        length = max(map(len, map(str, d.keys())))
        template = "{}\033[94m{{:{}}}\033[0m : {{}}\033[0m,".format(' ' * ti, length, base_indent)
        yield ' ' * base_indent + '{'
        for key, value in sorted(d.items()):
            if isinstance(value, (dict, tuple, list)):
                i = iter(beautify_iter(value, indent, base_indent + indent))
                v = next(i)[base_indent + indent:]
                yield template.format(key, v)
                yield from beautify_iter(value, indent, base_indent + indent)
            else:
                yield template.format(key, colored_type(value))
        yield ' ' * base_indent + '}' + (',' if base_indent else '')

    else:
        template = "{}{{}}\033[0m,".format(' ' * ti)
        yield ' ' * base_indent + '['
        for value in d:
            if isinstance(value, (dict, tuple, list)):
                yield from beautify_iter(value, indent, base_indent + indent)
            else:
                yield template.format(colored_type(value))
        yield ' ' * base_indent + ']' + (',' if base_indent else '')

def beautify(d, indent:int=4, base_indent:int=0):
    """Prints a dictionary in a colorful way."""
    for line in beautify_iter(d, indent, base_indent):
        print(line)

