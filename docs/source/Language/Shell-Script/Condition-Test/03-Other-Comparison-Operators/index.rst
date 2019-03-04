Other Comparison Operators
==============================================================================
.. contents::
    :local:
    :depth: 1

Reference: http://tldp.org/LDP/abs/html/comparison-ops.html


integer comparison
------------------------------------------------------------------------------
.. contents::
    :local:
    :depth: 1


``-eq`` is equal to
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``if [ "$a" -eq "$b" ]``


``-ne`` is not equal to
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``if [ "$a" -ne "$b" ]``


``-gt`` is greater than
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``if [ "$a" -gt "$b" ]``


``-ge`` is greater than or equal to
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``if [ "$a" -ge "$b" ]``


``-lt`` is less than
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``if [ "$a" -lt "$b" ]``


``-le`` is less than or equal to
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``if [ "$a" -le "$b" ]``


``<`` is less than (within double parentheses)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``(("$a" < "$b"))``


``<=`` is less than or equal to (within double parentheses)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``(("$a" <= "$b"))``


``>`` is greater than (within double parentheses)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``(("$a" > "$b"))``


``>=`` is greater than or equal to (within double parentheses)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``(("$a" >= "$b"))``


string comparison
------------------------------------------------------------------------------
.. contents::
    :local:
    :depth: 1


``==`` is equal to
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``if [ "$a" == "$b" ]``

This is a synonym for ``=``.

The == comparison operator behaves differently within a double-brackets test than within single brackets.

::

    [[ $a == z* ]]   # True if $a starts with an "z" (pattern matching).
    [[ $a == "z*" ]] # True if $a is equal to z* (literal matching).

    [ $a == z* ]     # File globbing and word splitting take place.
    [ "$a" == "z*" ] # True if $a is equal to z* (literal matching).


``!=`` is not equal to
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``if [ "$a" != "$b" ]``

This operator uses pattern matching within a [[ ... ]] construct.


``<`` is less than, in ASCII alphabetical order
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``if [[ "$a" < "$b" ]]``

``if [ "$a" \< "$b" ]``

Note that the ``<`` needs to be escaped within a ``[ ... ]`` construct.


``>`` is greater than, in ASCII alphabetical order
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``if [[ "$a" > "$b" ]]``

``if [ "$a" \> "$b" ]``

Note that the ``>`` needs to be escaped within a ``[ ... ]`` construct.


``-z`` string is null, that is, has zero length
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

    if [ -z "$String" ]
    then
      echo "\$String is null."
    else
      echo "\$String is NOT null."
    fi     # $String is null.


``-n`` string is not null.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Caution

.. warning::

    The -n test requires that the string be quoted within the test brackets. Using an unquoted string with ! -z, or even just the unquoted string alone within test brackets (see Example 7-6) normally works, however, this is an unsafe practice. **Always quote a tested string**.