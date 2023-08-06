import ast
import inspect
import re
import sys

from flake8_rst_docparams import __version__


def get_docparam(doc_line):
    m = re.match('^:param\s+([^:]+):\s*\S+', doc_line)
    if m:
        return m.groups()[0]


def doc_lines(obj):
    for sub in obj.body:
        # Detect documentation for function
        if type(sub) == ast.Expr and type(sub.value) == ast.Str:
            for doc_line in inspect.cleandoc(sub.value.s.replace('\r\n', '\n')).split('\n'):
                yield doc_line


cur_class_doc_params = set()


def traverse_ast(a, result=None, depth=0):
    global current_class_doc
    # Analyse the ast
    if result is None:
        result =  []
    for obj in a.body:
        if type(obj) == ast.ClassDef:
            current_class_doc = set()
            for doc_line in doc_lines(obj):
                cur_class_doc_params.add(get_docparam(doc_line))

        if type(obj) == ast.FunctionDef:
            arg_names = []
            has_return_val = True
            return_doc_found = False
            if hasattr(obj.returns, 'value'):
                if obj.returns.value == 'None':
                    has_return_val = False
            typ = 1 # Normal global function or static method
            for arg in obj.args.args:
                arg_names.append(arg.arg)
            try:
                arg_names.remove('self')
                typ = 2 # Class method
            except ValueError:
                pass
            if typ == 2 and obj.name == '__init__':
                # A classmethod and called __init__ (so constructor)
                typ = 3
                for param_doc in cur_class_doc_params:
                    if param_doc in arg_names:
                        arg_names.remove(param_doc)
            else:
                for doc_line in doc_lines(obj):
                    param_doc = get_docparam(doc_line)
                    return_doc_found |= re.match('^:return:\s*\S+', doc_line) is not None
                    if get_docparam(doc_line) in arg_names:
                        arg_names.remove(param_doc)
            for aname in arg_names:
                result.append((typ, obj.lineno, obj.name, aname))
            if has_return_val and not return_doc_found:
                result.append((4, obj.lineno, obj.name, ''))
        if hasattr(obj, 'body'):
            traverse_ast(obj, result, depth=depth+1)
    return result


def check_missing_docparams(fname):
    """
    Parse a python source file at ast-level to internally acknowledge which
    class methods will be bound to which classes.
    """
    # Create a source file parse-info-container and ast-parse the sourcefile
    src_info = {}
    src_fp = open(fname, 'rb')
    src = src_fp.read()
    src_fp.close()
    a = ast.parse(src)
    for missing_docparam in traverse_ast(a):
        yield (fname,) + missing_docparam


def gen_message(typ, argname, funcname, filename=None, lineno=None):
    if typ == 4:
        msg = f"Missing return documentation in function '{funcname}'"
    else:
        msg = f"Missing parameter documentation for '{argname}' in function '{funcname}'"
    msg = "DP%03i %s" % (typ, msg)
    if filename is not None and lineno is not None:
        msg = f"{filename}:{lineno}: {msg}"
    return msg


class CheckSource(object):

    name = "rst-docstrings"
    version = __version__

    def __init__(self, tree, filename="(none)"):
        """Initialise."""
        self.tree = tree
        self.filename = filename

    @classmethod
    def add_options(cls, parser):
        pass

    @classmethod
    def parse_options(cls, options):
        pass

    def run(self):
        for missing_docparam in check_missing_docparams(self.filename):
            assert 1, 1
            msg = gen_message(missing_docparam[1], missing_docparam[4], missing_docparam[3])
            yield missing_docparam[2], 0, msg, type(self)


if __name__ == '__main__':
    for a in sys.argv[1:]:
        for i in check_missing_docparams(a):
            print(gen_message(i[1], i[4], i[3], i[0], i[2]))
