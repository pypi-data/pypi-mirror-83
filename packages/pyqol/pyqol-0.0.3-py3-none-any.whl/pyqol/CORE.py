
import re
import functools
import inspect

#? Self-Modifying code
def codedit(find, replace, namespace=globals()):
    def wrapper(f):
        #! Only works for global functions !
        source_lines, _ = inspect.getsourcelines(f)
        while source_lines[0][0] == "@":
            source_lines = source_lines[1:]
        source = "".join(source_lines)
        new = re.sub(find, replace, source)
        exec(new)
        namespace[f.__name__] = eval(f.__name__)
        return namespace[f.__name__]
    return wrapper

#* Codedit modules
class Codedits():
    @staticmethod
    def Lambda(lambda_symbol):
        return codedit(r"{(.*)" + lambda_symbol + r"(.*)}", r"lambda \1: \2")
