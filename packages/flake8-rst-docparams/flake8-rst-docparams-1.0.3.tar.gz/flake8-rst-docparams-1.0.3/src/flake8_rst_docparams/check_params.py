import ast
import inspect
import re
import sys

from flake8_rst_docparams import __version__


def get_docparam(doc_line):
    m = re.match('^:param\s+([^:]+):.+', doc_line)
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
                    if get_docparam(doc_line) in arg_names:
                        arg_names.remove(param_doc)
            for aname in arg_names:
                result.append((typ, obj.lineno, obj.name, aname))
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
            msg = f"Missing parameter documentation for '{missing_docparam[4]}' in function '{missing_docparam[3]}'"
            msg = "DP%03i %s" % (missing_docparam[1], msg)
            assert 1, 1
            yield missing_docparam[2], 0, msg, type(self)


if __name__ == '__main__':
    for a in sys.argv[1:]:
        for i in check_missing_docparams(a):
            print(f"{i[0]}:{i[2]}:1: DP001 Missing parameter documentation for '{i[3]}' in function '{i[1]}'")
