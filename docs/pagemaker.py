import inspect
import importlib
import os

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
   :maxdepth: 1

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
   :show-inheritance:

"""


def ssorted(seq, **kwargs):
    key = kwargs['key']
    values = {}
    for item in seq:
        try:
            value = key(item)
            values[item] = value
        except TypeError:
            pass
    return sorted(values.iterkeys(), key=lambda item: values[item])


def module_doc(p):
    filepath = 'pages/api/' + p.__name__.replace('.', '-') + '.rst'
    names    = getattr(p, 'docs', [])
    attrs    = [importlib.import_module(p.__name__ + '.' + n) for n in names]
    modules  = [a for a in attrs if inspect.ismodule(a)]
    packages = [m for m in modules if m.__file__[-12:] == '__init__.pyc' or m.__file__[-11:] == '__init__.py']
    with open(filepath, 'w+') as fp:
        line = PACAKGE_PAGE.format(p.__name__, (p.__doc__ or '<docstring missing>'))
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
        clsss = None
        funcs = None
        with open(filepath, 'a') as fp:
            fp.write(SUBMODULE_SECTION.format(m.__name__, (m.__doc__ or '<docstring missing>')))
            names = getattr(m, 'docs', [])
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


def package_doc(package):
    filepath = 'pages/api/' + package.__name__.replace('.', '-') + '.rst'
    docs     = getattr(package, 'docs', [])
    names    = [n for doc in docs for n in doc]
    docs     = dict((n, doc[n]) for doc in docs for n in doc)
    objects  = dict((n, importlib.import_module(package.__name__ + '.' + n)) for n in names)
    modules  = [n for n in names if inspect.ismodule(objects[n])]
    packages = [n for n in modules if os.path.basename(objects[n].__file__) in ('__init__.pyc', '__init__.py')]
    with open(filepath, 'w+') as fp:
        fp.write(PACAKGE_PAGE.format(package.__name__, (package.__doc__ or '<...docstring missing...>')))
    if packages:
        with open(filepath, 'a') as fp:
            fp.write(SUBPACKAGES_SECTION)
            for n in packages:
                fp.write('   ' + objects[n].__name__.replace('.', '-') + '\n')
    for n in modules:
        if n in packages:
            continue
        items = docs[n]
        attrs = [getattr(objects[n], item) for item in items]
        clsss = [o for o in attrs if inspect.isclass(o)]
        funcs = [o for o in attrs if inspect.isfunction(o)]
        with open(filepath, 'a') as fp:
            fp.write(SUBMODULE_SECTION.format(objects[n].__name__, (objects[n].__doc__ or '<docstring missing>')))
            for o in clsss:
                n = o.__module__ + '.' + o.__name__
                fp.write('   ' + n.replace('.', '-') + '\n')
            for o in funcs:
                n = o.__module__ + '.' + o.__name__
                fp.write('   ' + n.replace('.', '-') + '\n')
            fp.write('\n')
        for o in clsss:
            class_doc(o)
        for f in funcs:
            function_doc(f)
    for name in packages:
        package_doc(objects[name])




def class_doc(c):
    bases = list(c.mro())
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
            if len(bases) > 1:
                for b in bases[1:]:
                    if hasattr(b, n):
                        return False
            return True
        return False
    def isclassmethod(n, o, c):
        if (inspect.ismethod(o) and
                not n.endswith('__') and
                n in c.__dict__ and
                type(c.__dict__[n]) == classmethod):
            return True
        return False
    def isnormalmethod(n, o, c):
        if (inspect.ismethod(o) and
                not n.endswith('__') and
                n in c.__dict__ and
                not type(c.__dict__[n]) == classmethod):
            return True
        return False
    def isdescriptor(n, o):
        if (inspect.isdatadescriptor(o) and
                not n.endswith('__') and
                n != 'args' and
                n != 'message'):
            if len(bases) > 1:
                for b in bases[1:]:
                    if hasattr(b, n):
                        return False
            return True
        return False
    members = inspect.getmembers(c)
    classattributes = [(n, o) for n, o in members if isclassattribute(n, o)]
    classmethods    = [(n, o) for n, o in members if isclassmethod(n, o, c)]
    specialmethods  = [(n, o) for n, o in members if isspecialmethod(n, o)]
    normalmethods   = [(n, o) for n, o in members if isnormalmethod(n, o, c)]
    descriptors     = [(n, o) for n, o in members if isdescriptor(n, o)]
    # classattributes = ssorted(classattributes, key=lambda m: inspect.getsourcelines(m[1])[1])
    # classmethods    = ssorted(classmethods, key=lambda m: inspect.getsourcelines(m[1])[1])
    # specialmethods  = ssorted(specialmethods, key=lambda m: inspect.getsourcelines(m[1])[1])
    # normalmethods   = ssorted(normalmethods, key=lambda m: inspect.getsourcelines(m[1])[1])
    classattributes = ssorted(classattributes, key=lambda m: m[0])
    classmethods    = ssorted(classmethods, key=lambda m: m[0])
    specialmethods  = ssorted(specialmethods, key=lambda m: m[0])
    normalmethods   = ssorted(normalmethods, key=lambda m: m[0])
    name = c.__module__ + '.' + c.__name__
    filepath = 'pages/api/' + name.replace('.', '-') + '.rst'
    with open(filepath, 'w+') as fp:
        fp.write(CLASS_PAGE.format(c.__name__, name))
        # class attributes
        fp.write('   .. rst-class:: class-section\n')
        fp.write('   .. rubric:: **Class attributes**\n\n')
        for n, o in classattributes:
            fp.write('   .. autoattribute:: {0}.{1}\n'.format(name, n))
        # class methods
        fp.write('   .. rst-class:: class-section\n')
        fp.write('   .. rubric:: **Class methods**\n\n')
        for n, o in classmethods:
            fp.write('   .. automethod:: {0}.{1}\n'.format(name, n))
        # descriptors
        fp.write('   .. rst-class:: class-section\n')
        fp.write('   .. rubric:: **Descriptors**\n\n')
        for n, o in descriptors:
            fp.write('   .. autoattribute:: {0}.{1}\n'.format(name, n))
        # special methods
        fp.write('   .. rst-class:: class-section\n')
        fp.write('   .. rubric:: **Magic methods**\n\n')
        for n, o in specialmethods:
            fp.write('   .. automethod:: {0}.{1}\n'.format(name, n))
        # normal methods
        fp.write('   .. rst-class:: class-section\n')
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

    #import sys
    #sys.path.append("C:/Users/rippmanm/workspace/brg_framework/src") 

    import brg
    import brg_rhino

    # reload(brg)
    # reload(brg_rhino)

    for doc in brg.docs:
        for name in doc:
            p = importlib.import_module(brg.__name__ + '.' + name)
            package_doc(p)
        # module_doc(p)

    # for name in brg_rhino.docs:
    #     p = importlib.import_module(brg_rhino.__name__ + '.' + name)
    #     module_doc(p)
