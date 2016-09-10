import inspect


def package_doc(p):
    with open('pages/' + p.__name__.replace('.', '-') + '.rst', 'w+') as fp:
        fp.write("""
********************************************************************************
{0}
********************************************************************************

{1}

""".format(p.__name__, p.__doc__))
        try:
            p_all = p.__all__
        except:
            p_all = []
        for name in p_all:
            m = getattr(p, name)
            if inspect.ismodule(m):
                fp.write("""
{0}
================================================================================

{1}

.. toctree::
   :glob:

""".format(m.__name__, m.__doc__))
                try:
                    m_all = m.__all__
                except:
                    m_all = []
                for name in m_all:
                    f = getattr(m, name)
                    if inspect.isfunction(f):
                        name = f.__module__ + '.' + f.__name__
                        fp.write('   ' + name.replace('.', '-') + '\n')
                fp.write('\n')


def module_doc(m):
    try:
        m_all = m.__all__
    except:
        m_all = []
    for name in m_all:
        o = getattr(m, name)
        if inspect.isfunction(o):
            name = o.__module__ + '.' + o.__name__
            with open('pages/' + name.replace('.', '-') + '.rst', 'w+') as fp:
                fp.write("""
********************************************************************************
{0}
********************************************************************************

.. autofunction:: {1}

""".format(o.__name__, name))


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import brg

    for name in brg.__all__:
        p = getattr(brg, name)
        package_doc(p)
        if not hasattr(p, '__all__'):
            print 'package {0} has no __all__'.format(p)
            continue
        for name in p.__all__:
            m = getattr(p, name)
            if inspect.ismodule(m):
                if not hasattr(m, '__all__'):
                    print 'module {0} has no __all__'.format(m)
                module_doc(m)
