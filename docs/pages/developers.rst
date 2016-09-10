.. _developers:

********************************************************************************
Developers Guide
********************************************************************************


How to contribute
================================================================================

The BRG framework is hosted on bitbucket as a public repository.
Therefore any bitbucket user may create a branch and submit a pull request.

.. todo::
    
    Explain how to do this.


Coding standards
================================================================================

The BRG framework is coded according to the `PEP8 -- Style Guide for Python Code <https://www.python.org/dev/peps/pep-0008/>`_.

.. todo::

    Provide brief overview of what that means.


Naming conventions
================================================================================

- class names: CamelCase
- method names: snake_case
- function names: snake_case
- variable names: snake_case
- module-level variables: UPPERCASE
- boolean variables: ``is_...``, ``has_...``, ``can_...``
- boolean valued functions or methods: xxx
- ...

.. todo::
    
    Expand and provide examples.


Packages and Subpackages
================================================================================

- Nest as deep as necessary.
- Pull common functions up to second level.
- ...


Templates and Snippets
================================================================================

The BRG framework contains many templates and snippets for Eclipse, Sublime, and Atom.
they can be found in the templates folder.

.. todo::

    Provide a list of templates and snippets.

.. todo::

    Provide instructions on how to use them.


Folder structure
================================================================================

- ...


Documentation
================================================================================

- Documentation generated with Sphinx.
- Google style docstring support through the napoleon package.
- Package and module documentation pages generated with custom script

.. code-block:: python
    :linenos:

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
