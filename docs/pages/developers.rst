.. _developers:

********************************************************************************
Developers Guide
********************************************************************************

.. note::
    
    Add something about data storage: json in combination with from/to functions, not pickle



How to contribute
================================================================================

The BRG framework is hosted on bitbucket as a public repository.
Therefore any bitbucket user may create a branch and submit a pull request.


Coding standards
================================================================================

The BRG framework is coded according to the `PEP8 -- Style Guide for Python Code <https://www.python.org/dev/peps/pep-0008/>`_.


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


Packages and Subpackages
================================================================================

- Nest as deep as necessary.
- Pull common functions up to second level.
- ...


Templates and Snippets
================================================================================

The BRG framework contains many templates and snippets for Eclipse, Sublime, and Atom.
they can be found in the templates folder.


Documentation
================================================================================

- Docstrings!
- Documentation generated with Sphinx.
- Google style docstring support through the napoleon package.
- Package and module documentation pages generated with custom script

