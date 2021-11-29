#!/usr/bin/env python3

"""Command line interface to query the stock.

To iterate the source data you can use the following structure:

for item in warehouse1:
    # Your instructions here.
    # The `item` name will contain each of the strings (item names)
        in the list.
"""

from loader import Loader
import argparse
from classes import User
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


# Setting up the basic parameters
def __initialize():
    stock = Loader(model="stock")
    personnel, usr = __hello()
    return {
        'staff': personnel,
        'warehouses': stock,
        'user': usr,
    }


# Greet the user
def __hello():
    personnel = Loader(model="personnel")
    if parser.parse_args().name:
        name = parser.parse_args().name
    else:
        name = input("Please enter your name: ")
    for employee in personnel:
        if employee.is_named(name):
            usr = employee
            break
    else:
        usr = User(name)
    usr.greet()
    return personnel, usr


# Presents the user's choices
def __choice(variables):
    opt = input(
        "What would you like to do?\n" +
        "1. List items by warehouse.\n" +
        "2. Search an item and place an order.\n" +
        "3. Browse by category\n" +
        "4. Quit.\n" +
        "Type the number of the operation: "
    )
    if opt == "1":
        __print_all(variables)
    elif opt == "2":
        __browse_items(variables)
    elif opt == "3":
        __browse_categories(variables)
    elif opt == "4":
        return False
    else:
        print(f"{opt} is not a valid operation.")
        __choice(variables)
        return
    return __da_capo()


# List all items by warehouse
def __print_all(variables):
    for warehouse in variables['warehouses']:
        print(f"----------\nItems in {warehouse}\n----------")
        for item in warehouse.get_items():
            print(f'- {item}')
    total = 0
    for warehouse in variables['warehouses']:
        total += warehouse.occupancy()
        print(f"Total items in {warehouse}: {warehouse.occupancy()}")
    variables['user'].update_log(f'Listed {total} items from all warehouses.')


# Browses the warehouses for one item
def __browse_items(variables):
    wish = input("What is the name of the item? ")
    item_list = [wh.search(wish) for wh in variables['warehouses']]
    amount = [len(wh) for wh in item_list]
    total_amount = sum(amount)
    variables['user'].update_log(f'Searched for {wish}.')
    print(f"Amount available: {total_amount}")
    if len(amount) - amount.count(0) > 1:
        print("Location:")
        for i, items in enumerate(item_list):
            if items:
                for item in [
                    x for x in sorted(
                        items,
                        key=lambda x: dt.now() - dt.fromisoformat(
                            x.date_of_stock
                        )
                    )
                ]:
                    stocked = (
                        dt.now() - dt.fromisoformat(
                            item.date_of_stock
                        )
                    ).days
                    print(f"- Warehouse {i + 1} (in stock for {stocked} days)")
                print()
        max_amount = max(amount)
        if amount.count(max_amount) == 1:
            print(f"Maximum availability: {max_amount} in Warehouse {amount.index(max_amount) + 1}.")
        else:
            print(f"The following Warehouses have the maximum availability of {max_amount} in store:")
            for i, num in enumerate(amount):
                if num == max_amount:
                    print(f"- Warehouse {i + 1}")
        __order(variables, amount, wish)
    elif len(amount) - amount.count(0) == 1:
        for i, num in enumerate(amount):
            if num != 0:
                print(f"Location: Warehouse {i + 1}")
        __order(variables, amount, wish)
    else:
        print("Location: Not in stock")


# Browses the warehouses by its categories
def __browse_categories(variables):
    categories = dict()
    for wh in variables['warehouses']:
        for item in wh.get_items():
            try:
                categories[item.category].append(item)
            except KeyError:
                categories[item.category] = [item]
    cats = [(k, len(v)) for k, v in reversed(sorted(
        categories.items(), key=lambda cat: len(cat[1])
    ))]
    for i, category in enumerate(cats):
        print(f"{i + 1}. {category[0]} ({category[1]})")
    while True:
        cat = input("Type the number of the category to browse: ")
        try:
            choice = cats[int(cat)][0]
            print(f"List of {choice}s available:")
            break
        except TypeError:
            print("Please only type the category number.")
        except IndexError:
            print("Please select one of the displayed numbers.")
    for item in [
        x for x in sorted(
            categories[choice],
            key=lambda x: x.warehouse
        )
    ]:
        print(
            f"{item},",
            f"Warehouse {item.warehouse}",
        )
    variables['user'].update_log(f'Browsed the category {choice}.')


# Given the requested item and the listed availibilities, order some of the
# items
def __order(variables, amount, wish):
    order = input(f"Would you like to order {wish}?(y/n) ")
    if order.lower() == "y":
        if type(variables['user']) is User:
            print('This option is only available for Employees.\nOrder process aborted.')
            return
        while not variables['user'].is_authenticated:
            pw = input('Please enter your password. Leave empty to abort the order process: ')
            if not pw:
                print('Order process aborted.')
                return
            variables['user'].authenticate(pw)
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
                variables['user'].order(wish, max_order)
            else:
                print("Order process aborted.")
        else:
            variables['user'].order(wish, order_amount)
        variables['user'].update_log(f'Ordered {order_amount} of {wish}.')


# Check if another operation is desired
def __da_capo():
    cont = input("Do you wish to perform another operation?(y/n) ")
    if cont == "y":
        return True
    return False


# Say goodbye to the user
def __goodbye(variables):
    variables['user'].bye()


# The active script to be called
def script():
    variables = __initialize()
    da_capo = True
    while da_capo:
        da_capo = __choice(variables)
    __goodbye(variables)


script()
