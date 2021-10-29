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

# Converting stock to usable lists
warehouses = [[], []]
for item in stock:
    if item['warehouse'] == 1:
        warehouses[0].append(item)
    else:
        warehouses[1].append(item)

# Get the user name
if parser.parse_args().name:
    usr = parser.parse_args().name
else:
    usr = input("Please enter your name: ")

# Greet the user
print(f"Hello, {usr}.")

# Show the menu and ask to pick a choice
while True:
    opt = input(
        "What would you like to do?\n" +
        "1. List items by warehouse.\n" +
        "2. Search an item and place an order.\n" +
        "3. Browse by category\n" +
        "4. Quit.\n" +
        "Type the number of the operation: "
    )

# If they pick 1
    if opt == "1":
        for i in range(2):
            print(f"----------\nItems in Warehouse {i + 1}\n----------")
            for item in set(
                [f"{x['state']} {x['category']}" for x in warehouses[i]]
            ):
                print(f"- {item}")
        for i in range(2):
            print(f"Total items in warehouse {i + 1}: {len(warehouses[i])}")

# Else, if they pick 2
    elif opt == "2":
        wish = input("What is the name of the item? ")
        wishes = [[], []]
        for i in range(2):
            for x in warehouses[i]:
                if f"{x['state']} {x['category']}".lower() == wish.lower():
                    wishes[i].append(x)
        amount = [len(wishes[0]), len(wishes[1])]
        max_amount = sum(amount)
        print(f"Amount available: {max_amount}")
        if amount[0] and amount[1]:
            print("Location:")
            for i in range(2):
                for item in [
                        x for x in sorted(
                            wishes[i],
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
            if amount[0] > amount[1]:
                print(f"Maximum availability: {amount[0]} in Warehouse 1.")
            elif amount[0] < amount[1]:
                print(f"Maximum availability: {amount[1]} in Warehouse 2.")
            else:
                print(f"Both Warehouses have {amount[0]} in store.")
        elif amount[0]:
            print("Location: Warehouse 1")
        elif amount[1]:
            print("Location: Warehouse 2")
        else:
            print("Location: Not in stock")
            cont = input("Do you wish to perform another operation?(y/n) ")
            if cont.lower() == "y":
                continue
            else:
                break
        order = input(f"Would you like to order {wish}?(y/n) ")
        if order.lower() == "y":
            while True:
                try:
                    order_amount = int(input("How many would you like? "))
                    break
                except ValueError:
                    print("Please enter a number.")
            if order_amount > max_amount:
                print(f"-------\nMax order amount is {max_amount}.\n-------")
                max_order = input(f"Order {max_amount} of '{wish}'?(y/n) ")
                if max_order:
                    print(f"{max_amount} of '{wish}' have been ordered.")
            else:
                print(f"{order_amount} of '{wish}' have been ordered.")

# Else, if they pick 3
    elif opt == "3":
        categories = dict()
        for item in stock:
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

# Else, if they pick 4
    elif opt == "4":
        break
# Else
    else:
        print(f"{opt} is not a valid operation.")
        continue
    cont = input("Do you wish to perform another operation?(y/n) ")
    if cont.lower() != "y":
        break


# Thank the user for the visit
print(f"Thank you for your visit, {usr}.")
