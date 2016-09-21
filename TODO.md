# brg framework: todo

- connection to ShapeOp
- connection to igl library
- integration of C/C++ code
    
    For example, using ``scipy.weave``.
    Other options?

- compare performance of descriptors and functions
- rhino brg plugins (c# and c++)
- maya brg plugin (c++)
- document the returning of ``None``?
- separate **all** viewer functionality into brg_viewer?
- use something other than ``__all__`` to base docs on. for example, ``_all_``
    
    Otherwise only functionality that is completely platform independent can be
    documented. The same is true for algorithms and operations that are based on
    ``scipy``, or other strictly *CPython* functionality.

- *collapse* functions of class definition by default => provide overview...
- add docstrings before/in/after definitions?
