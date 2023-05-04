Python Requirements.txt Syntax
==============================================================================
Keywords: Python, Requirements

Example::

    SomeProject
    SomeProject == 1.3
    SomeProject >= 1.2, < 2.0
    SomeProject[foo, bar]
    SomeProject ~= 1.4.2
    SomeProject == 5.4 ; python_version < '3.8'
    SomeProject ; sys_platform == 'win32'
    requests [security] >= 2.8.1, == 2.8.* ; python_version < "2.7"

Reference:

- `Requirement Specifiers <https://pip.pypa.io/en/stable/reference/requirement-specifiers/>`_: requirements.txt spec in pip document
- `PEP 440 – Version Identification and Dependency Specification <https://peps.python.org/pep-0440/#version-specifiers>`_: related PEP 440 standard created in 2013-03-18
