Shell Script - List
==============================================================================


For Loop:

.. code-block:: bash

    #!/bin/bash

    # construct a list this way:
    text="a b c d e f g"
    words=($text)

    # or this:
    #words=(a b c d e f g)

    # or this:
    #words=("a" "b" "c" "d" "e" "f" "g")

    for i in "${words[@]}"
    do
        echo $i
    done

Slice:

.. code-block:: bash

    #!/bin/bash

    # the syntax ${var[@]: start_index:n_item}, from <start_index> index, select <n_item> items.
    words=(0 1 2 3 4 5 6 7 8 9)

    #---
    echo ${words[@]: 0:1} # first item: 0
    echo ${words[@]: 1:1} # second item: 1
    echo ${words[@]: -1:1} # last: 9
    echo ${words[@]: -2:1} # second last: 8

    #---
    echo ${words[@]: 3:5} # from index 3, select 5 items: 3 4 5 6 7
    echo ${words[@]: -7:5} # from index -7, select 5 items: 3 4 5 6 7
    start_index=3
    n_item=5
    echo ${words[@]: $start_index:$n_item} # from index 3, select 6 items: 3 4 5 6 7

    #---
    echo ${words[0]} # first item: 0
    echo ${words[1]} # second item: 1
    nth=2
    echo ${words[$nth]} # third item: 2

    #---
    items=${words[@]: 3:5} # 3 4 5 6 7
    items=($items) # construct a list
    for i in "${items[@]}"
    do
        echo $i
    done
