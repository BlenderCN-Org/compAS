import inspect

# 0: brg.com.__name__
# 1: brg.com.__doc__
#
# append: subpackages section
# append: module sections
PACAKGE_PAGE = """
********************************************************************************
{0}
********************************************************************************

{1}

"""

SUBPACKAGES_SECTION = """

.. rubric:: **Subpackages**

.. toctree::
   :glob:
   :maxdepth: 3

"""

# 0: brg.com.matlab.engine.__name__
# 1: brg.com.matlab.engine.__doc__
SUBMODULE_SECTION = """

{0}
================================================================================

{1}

.. toctree::
   :glob:

"""

# 0: brg.geometry.functions.cross.__name__
FUNCTION_PAGE = """
********************************************************************************
{0}
********************************************************************************

.. autofunction:: {1}

"""


def module_doc(p):
    filepath = 'pages/api/' + p.__name__.replace('.', '-') + '.rst'
    names    = getattr(p, '__all__', [])
    attrs    = [getattr(p, n) for n in names]
    modules  = [a for a in attrs if inspect.ismodule(a)]
    packages = [m for m in modules if m.__file__[-12:] == '__init__.pyc' or m.__file__[-11:] == '__init__.py']
    print packages
    # create a package.rst file
    # and write the package header
    with open(filepath, 'w+') as fp:
        line = PACAKGE_PAGE.format(p.__name__, p.__doc__)
        fp.write(line)
    if packages:
        # append a subpackages section to the package file
        # add an entry to the toctree per subpackage
        with open(filepath, 'a') as fp:
            fp.write(SUBPACKAGES_SECTION)
            for m in packages:
                line = '   ' + m.__name__.replace('.', '-') + '\n'
                fp.write(line)
    for m in modules:
        if m in packages:
            continue
        # for every module that is not a package
        # append a module section
        # add an entry to the toctree per function in the module
        funcs = None
        with open(filepath, 'a') as fp:
            fp.write(SUBMODULE_SECTION.format(m.__name__, m.__doc__))
            names = getattr(m, '__all__', [])
            attrs = [getattr(m, n) for n in names]
            funcs = [a for a in attrs if inspect.isfunction(a)]
            clsss = [a for a in attrs if inspect.isclass(a)]
            for c in clsss:
                name = c.__module__ + '.' + c.__name__
                line = '   ' + name.replace('.', '-') + '\n'
                fp.write(line)
            for f in funcs:
                name = f.__module__ + '.' + f.__name__
                line = '   ' + name.replace('.', '-') + '\n'
                fp.write(line)
            fp.write('\n')
        if clsss:
            for c in clsss:
                function_doc(c)
        if funcs:
            for f in funcs:
                function_doc(f)
    for m in packages:
        module_doc(m)


def function_doc(f):
    name = f.__module__ + '.' + f.__name__
    filepath = 'pages/api/' + name.replace('.', '-') + '.rst'
    with open(filepath, 'w+') as fp:
        fp.write(FUNCTION_PAGE.format(f.__name__, name))
    return


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import brg

    for name in brg.__all__:
        p = getattr(brg, name)
        module_doc(p)
