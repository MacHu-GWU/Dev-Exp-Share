
Relational DB
------------------------------------------------------------------------------
recipe_and_ingredient
    recipe_id
    ingredient_id


Find ingredient list by recipe
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: SQL

    SELECT
        T.ingredient_id
    FROM recipe_and_ingredient T
    WHERE T.recipe_id = :recipe_id


Given set of ingredient, find recipe you can do
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: SQL

    sql =

    SELECT
        T.receipt_id,
        string_agg(T.ingredient_id, "-"),
    FROM recipe_and_ingredient T
    GROUP BY T.recipe_id

    given_ingredient_id_set = ...
    doable_receipt_id_list = list()
    for receipt_id, ingredient_keys in engine.execute(sql):
        ingredient_id_set = set(ingredient_keys.split("-"))
        if ingredient_id_set.is_subset(given_ingredient_id_set):
            doable_receipt_id_list.append(receipt_id)
