import inspect

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

SUBMODULE_SECTION = """

{0}
================================================================================

{1}

.. toctree::
   :glob:

"""

FUNCTION_PAGE = """
********************************************************************************
{0}
********************************************************************************

.. autofunction:: {1}

"""

CLASS_PAGE = """
********************************************************************************
{0}
********************************************************************************

.. autoclass:: {1}

"""


def module_doc(p):
    filepath = 'pages/api/' + p.__name__.replace('.', '-') + '.rst'
    names    = getattr(p, '__all__', [])
    attrs    = [getattr(p, n) for n in names]
    modules  = [a for a in attrs if inspect.ismodule(a)]
    packages = [m for m in modules if m.__file__[-12:] == '__init__.pyc' or m.__file__[-11:] == '__init__.py']
    with open(filepath, 'w+') as fp:
        line = PACAKGE_PAGE.format(p.__name__, p.__doc__)
        fp.write(line)
    if packages:
        with open(filepath, 'a') as fp:
            fp.write(SUBPACKAGES_SECTION)
            for m in packages:
                line = '   ' + m.__name__.replace('.', '-') + '\n'
                fp.write(line)
    for m in modules:
        if m in packages:
            continue
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
                class_doc(c)
        if funcs:
            for f in funcs:
                function_doc(f)
    for m in packages:
        module_doc(m)


def class_doc(c):
    def isclassattribute(n, o):
        if (not inspect.ismethod(o) and
                not inspect.isbuiltin(o) and
                not inspect.ismethoddescriptor(o) and
                not inspect.isdatadescriptor(o) and
                not inspect.isgetsetdescriptor(o) and
                not inspect.ismemberdescriptor(o) and
                not n.endswith('__')):
            return True
        return False
    def isspecialmethod(n, o):
        if (inspect.ismethod(o) and
                n.endswith('__') and
                n != '__init__'):
            return True
        return False
    def isclassmethod(n, o, c):
        if (inspect.ismethod(o) and
                not n.endswith('__') and
                type(c.__dict__[n]) == classmethod):
            return True
        return False
    def isnormalmethod(n, o, c):
        if (inspect.ismethod(o) and
                not n.endswith('__') and
                not type(c.__dict__[n]) == classmethod):
            return True
        return False
    def isdescriptor(n, o):
        if (inspect.isdatadescriptor(o) and
                not n.endswith('__') and
                n != 'args' and
                n != 'message'):
            return True
        return False
    members = inspect.getmembers(c)
    classattributes = [(n, o) for n, o in members if isclassattribute(n, o)]
    classmethods    = [(n, o) for n, o in members if isclassmethod(n, o, c)]
    specialmethods  = [(n, o) for n, o in members if isspecialmethod(n, o)]
    normalmethods   = [(n, o) for n, o in members if isnormalmethod(n, o, c)]
    descriptors     = [(n, o) for n, o in members if isdescriptor(n, o)]
    classattributes = sorted(classattributes, key=lambda m: inspect.getsourcelines(m[1])[1])
    classmethods    = sorted(classmethods, key=lambda m: inspect.getsourcelines(m[1])[1])
    specialmethods  = sorted(specialmethods, key=lambda m: inspect.getsourcelines(m[1])[1])
    normalmethods   = sorted(normalmethods, key=lambda m: inspect.getsourcelines(m[1])[1])
    name = c.__module__ + '.' + c.__name__
    filepath = 'pages/api/' + name.replace('.', '-') + '.rst'
    with open(filepath, 'w+') as fp:
        fp.write(CLASS_PAGE.format(c.__name__, name))
        # class attributes
        fp.write('   .. rubric:: **Class attributes**\n\n')
        for n, o in classattributes:
            fp.write('   .. autoattribute:: {0}.{1}\n'.format(name, n))
        # class methods
        fp.write('   .. rubric:: **Class methods**\n\n')
        for n, o in classmethods:
            fp.write('   .. automethod:: {0}.{1}\n'.format(name, n))
        # descriptors
        fp.write('   .. rubric:: **Descriptors**\n\n')
        for n, o in descriptors:
            fp.write('   .. autoattribute:: {0}.{1}\n'.format(name, n))
        # special methods
        fp.write('   .. rubric:: **Special methods**\n\n')
        for n, o in specialmethods:
            fp.write('   .. automethod:: {0}.{1}\n'.format(name, n))
        # normal methods
        fp.write('   .. rubric:: **Methods**\n\n')
        for n, o in normalmethods:
            fp.write('   .. automethod:: {0}.{1}\n'.format(name, n))


def function_doc(f):
    name = f.__module__ + '.' + f.__name__
    filepath = 'pages/api/' + name.replace('.', '-') + '.rst'
    with open(filepath, 'w+') as fp:
        fp.write(FUNCTION_PAGE.format(f.__name__, name))


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import brg
    # import brg_rhino

    reload(brg)
    # reload(brg_rhino)

    for name in brg.__all__:
        p = getattr(brg, name)
        module_doc(p)
