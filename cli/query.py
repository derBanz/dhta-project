#!/usr/bin/env python3

"""Command line interface to query the stock.

To iterate the source data you can use the following structure:

for item in warehouse1:
    # Your instructions here.
    # The `item` name will contain each of the strings (item names)
        in the list.
"""

from data import stock
import argparse
from datetime import datetime as dt

# YOUR CODE STARTS HERE

# Using command line arguments
parser = argparse.ArgumentParser(
    description="Consult items in stock and place orders."
)
parser.add_argument(
    "name",
    metavar="NAME",
    type=str,
    nargs="?",
    help="Name of User (optional)"
)


# Warehouse class
class Warehouse:
    def __init__(self, number):
        self.stock = list()
        self.number = number

    def __iter__(self):
        return iter(self.stock)

    def __len__(self):
        return len(self.stock)

    def get_items(self):
        return self.stock

    def add_item(self, item):
        self.stock.append(item)


# Browses the warehouses by its categories
def __browse_categories(warehouses):
    categories = dict()
    for wh in warehouses:
        for item in wh:
            try:
                categories[item['category']].append(item)
            except KeyError:
                categories[item['category']] = [item]
    cats = [(k, len(v)) for k, v in reversed(sorted(
        categories.items(), key=lambda cat: len(cat[1])
    ))]
    for i in range(len(cats)):
        print(f"{i + 1}. {cats[i][0]} ({cats[i][1]})")
    while True:
        cat = input("Type the number of the category to browse: ")
        try:
            print(f"List of {cats[int(cat)][0]}s available:")
            break
        except TypeError:
            print("Please only type the category number.")
        except IndexError:
            print("Please select one of the displayed numbers.")
    for item in [
        x for x in sorted(
            categories[cats[int(cat)][0]],
            key=lambda x: x['warehouse']
        )
    ]:
        print(
            f"{item['state']} {item['category']},",
            f"Warehouse {item['warehouse']}",
        )


# Browses the warehouses for one item
def __browse_items(warehouses):
    wish = input("What is the name of the item? ")
    items = __search_item(warehouses, wish)
    amount = [len(items[i]) for i in range(len(warehouses))]
    total_amount = sum(amount)
    print(f"Amount available: {total_amount}")
    if len(amount) - amount.count(0) > 1:
        print("Location:")
        for i in range(len(amount)):
            if amount[i] != 0:
                for item in [
                    x for x in sorted(
                        items[i],
                        key=lambda x: dt.now() - dt.fromisoformat(
                            x['date_of_stock']
                        )
                    )
                ]:
                    stocked = (
                        dt.now() - dt.fromisoformat(
                            item['date_of_stock']
                        )
                    ).days
                    print(f"- Warehouse {i + 1} (in stock for {stocked} days)")
                print()
        max_amount = max(amount)
        if amount.count(max_amount) == 1:
            print(f"Maximum availability: {max_amount} in Warehouse {amount.index(max_amount) + 1}.")
        else:
            print(f"The following Warehouses have the maximum availability of {max_amount} in store:")
            for i in range(len(amount)):
                if amount[i] > 0:
                    print(f"- Warehouse {i + 1}")
        __order(amount, wish)
    elif len(amount) - amount.count(0) == 1:
        for i in range(len(amount)):
            if amount[i] != 0:
                print(f"Location: Warehouse {i + 1}")
        __order(amount, wish)
    else:
        print("Location: Not in stock")


# Presents the user's choices
def __choice(warehouses):
    opt = input(
        "What would you like to do?\n" +
        "1. List items by warehouse.\n" +
        "2. Search an item and place an order.\n" +
        "3. Browse by category\n" +
        "4. Quit.\n" +
        "Type the number of the operation: "
    )
    if opt == "1":
        __print_all(warehouses)
    elif opt == "2":
        __browse_items(warehouses)
    elif opt == "3":
        __browse_categories(warehouses)
    elif opt == "4":
        return False
    else:
        print(f"{opt} is not a valid operation.")
        __choice()
        return
    return __da_capo()


# One time use to build a list of warehouse-items
def __create_warehouses():
    warehouses = list()
    for item in sorted(stock, key=lambda thing: thing['warehouse']):
        if item['warehouse'] > len(warehouses):
            warehouses.append(Warehouse(item['warehouse']))
        warehouses[item['warehouse'] - 1].add_item(item)
    return warehouses


# Check if another operation is desired
def __da_capo():
    cont = input("Do you wish to perform another operation?(y/n) ")
    if cont == "y":
        return True
    return False


# Say goodbye to the user
def __goodbye(usr):
    print(f"Thank you for your visit, {usr}.")


# Greet the user
def __hello():
    if parser.parse_args().name:
        usr = parser.parse_args().name
    else:
        usr = input("Please enter your name: ")
    print(f"Hello, {usr}.")
    return usr


# Given the requested item and the listed availibilities, order some of the
# items
def __order(amount, wish):
    order = input(f"Would you like to order {wish}?(y/n) ")
    if order.lower() == "y":
        max_amount = sum(amount)
        while True:
            try:
                order_amount = int(input("How many would you like? "))
                break
            except ValueError:
                print("Please enter a number.")
        if order_amount > max_amount:
            print(f"-------\nMax order amount is {max_amount}.\n-------")
            max_order = input(f"Order {max_amount} of '{wish}'?(y/n) ")
            if max_order.lower() == "y":
                print(f"{max_amount} of '{wish}' have been ordered.")
            else:
                print("Order process aborted.")
        else:
            print(f"{order_amount} of '{wish}' have been ordered.")


# List all items by warehouse
def __print_all(warehouses):
    for i in range(len(warehouses)):
        print(f"----------\nItems in Warehouse {i + 1}\n----------")
        for item in set(
            [f"{x['state']} {x['category']}" for x in warehouses[i]]
        ):
            print(f"- {item}")
    for i in range(len(warehouses)):
        print(f"Total items in warehouse {i + 1}: {len(warehouses[i])}")


# Build a list of items per warehouse that fit the query
def __search_item(warehouses, wish):
    wishes = [[] for warehouse in warehouses]
    for i in range(len(warehouses)):
        for x in warehouses[i]:
            if f"{x['state']} {x['category']}".lower() == wish.lower():
                wishes[i].append(x)
    return wishes


# The active script to be called
def script():
    warehouses = __create_warehouses()
    usr = __hello()
    da_capo = True
    while da_capo:
        da_capo = __choice(warehouses)
    __goodbye(usr)


script()
