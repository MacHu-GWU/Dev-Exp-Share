Choose-Dataclass-and-Validation-Library
==============================================================================
**Candidates**

- `marshmallow <https://marshmallow.readthedocs.io/en/stable/>`_: validation and serialization framework, created on 2013.
- `attrs <https://www.attrs.org/en/stable/index.html>`_: writing python class, simple validation, simple serialization, created on 2015.
- `pydantic <https://pydantic-docs.helpmanual.io/usage/validators/>`_: validation library based on type hint, created on 2017.
- `dataclasses <https://docs.python.org/3/library/dataclasses.html>`_: Python3.7 standard library for data class, created on 2018.


**Highlight**

In this section, I show the best part of each library that completely beat others:

- marshmallow: no intrusion to your existing code, the capability to extend and customization is the best.
- attrs: mature, zero dependency, support the most of Python versions, including PyPy. has all features, and be capable to extend.
- pydantic: strongly depends on type hint, fast.
- dataclasses: standard library, no need to install anything.

**Deal Breaker**

In this section, I show the strong reason NOT use each library.

- marshmallow: it cannot help you writing your data class
- attrs: NO
- pydantic: you need to work under <= 3.6.
- dataclasses: you need custom validation.
