import csv
import timeit
# noinspection PyUnresolvedReferences
from BTrees.OOBTree import OOBTree

# Створення OOBTree
tree = OOBTree()

# Додавання елементів до дерева
def add_item_to_tree(item: dict):
    tree.update({ int(item["ID"]): item})

# Виведення товарів у діапазоні цін
def range_query_tree(min_price: float, max_price: float) -> list:
    res = []
    for key, item in tree.items():
        if min_price <= float(item["Price"]) <= max_price:
            res.append(item)
    return res

# Створення словника
dictionary = dict()

def add_item_to_dict(item: dict):
    dictionary[int(item["ID"])] = item

def range_query_dict(min_price: float, max_price: float):
    res = []
    for item in dictionary.values():
        if min_price <= float(item["Price"]) <= max_price:
            res.append(item)
    return res

# Заповнимо дерево і словник даними з файлу
with open('generated_items_data.csv', mode='r') as file:
    csvFile = csv.DictReader(file)
    for item in csvFile:
        add_item_to_tree(item)
        add_item_to_dict(item)

SETUP_CODE = '''
from __main__ import range_query_tree, range_query_dict
'''

print("Total range_query time for OOBTree:",
      timeit.timeit(setup=SETUP_CODE,
                    stmt='range_query_tree(40, 50)',
                    number=100),
      "seconds")
print("Total range_query time for Dict:",
      timeit.timeit(setup=SETUP_CODE,
                    stmt='range_query_dict(40, 50)',
                    number=100),
      "seconds")