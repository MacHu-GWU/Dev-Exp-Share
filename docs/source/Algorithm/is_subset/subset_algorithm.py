# -*- coding: utf-8 -*-

"""
use prime key trick to check is_subset

conclusion, still slower than built-in set.issubset method
"""

from datetime import datetime
import uuid
import random
import json


def multiply_list(l):
    # Multiply elements one by one
    result = 1
    for x in l:
        result = result * x
    return result


with open("first_10000_prime.json", "r") as f:
    first_10000_prime = json.loads(f.read())
    prime_mapper = {ind: prime for ind, prime in enumerate(first_10000_prime)}

n_ingredient = 10000
n_receipt = 50000
n_given_ingredient = 15

random_10000_str = [str(uuid.uuid4()) for _ in range(n_ingredient)]
key_to_prime = {key: prime for key, prime in zip(random_10000_str, first_10000_prime)}

recipe_ingredient_key_set_list = list()
recipe_ingredient_prime_key_list = list()

for _ in range(n_receipt):
    ingredient_key_list = random.sample(random_10000_str, random.randint(1, 10))
    recipe_ingredient_key_set_list.append(set(ingredient_key_list))
    recipe_ingredient_prime_key_list.append(
        multiply_list([key_to_prime[key] for key in ingredient_key_list])
    )

print(recipe_ingredient_key_set_list[:3])
print(recipe_ingredient_prime_key_list[:3])

ingredient_key_list = random.sample(random_10000_str, n_given_ingredient)
ingredient_key_set = set(ingredient_key_list)
ingredient_prime_key = multiply_list([key_to_prime[key] for key in ingredient_key_list])

# use python built-in set
st = datetime.now()
result1 = list()
for ind, recipe_ingredient_key_set in enumerate(recipe_ingredient_key_set_list):
    if recipe_ingredient_key_set.issubset(ingredient_key_set):
        result1.append(ind)
elapse1 = (datetime.now() - st).total_seconds()

# use prime key
st = datetime.now()
result2 = list()
for ind, recipe_ingredient_prime_key in enumerate(recipe_ingredient_prime_key_list):
    if ingredient_prime_key % recipe_ingredient_prime_key == 0:
        result2.append(ind)
elapse2 = (datetime.now() - st).total_seconds()

print(result1)
print(result2)
print(elapse1)
print(elapse2)
