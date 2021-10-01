#!/usr/bin/env python3

"""Command line interface to query the stock.

To iterate the source data you can use the following structure:

for item in warehouse1:
    # Your instructions here.
    # The `item` name will contain each of the strings (item names)
        in the list.
"""

from data import warehouse1, warehouse2
import argparse

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
        "3. Quit.\n" +
        "Type the number of the operation: "
    )

# If they pick 1
    if opt == "1":
        for i in range(2):
            print(f"-------\nItems in Warehouse {i + 1}\n-------")
            for item in [warehouse1, warehouse2][i]:
                print(f"- {item}")

# Else, if they pick 2
    elif opt == "2":
        item = input("What is the name of the item? ")
        warehouses = [
            warehouse1,
            warehouse2
        ]
        amount = [0, 0]
        for i in range(2):
            amount[i] = warehouses[i].count(item)
        max_amount = sum(amount)
        print(f"Amount available: {max_amount}")
        if amount[0] and amount[1]:
            print("Location: Both warehouses")
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
        order = input(f"Would you like to order {item}?(y/n) ")
        if order.lower() == "y":
            while True:
                try:
                    order_amount = int(input("How many would you like? "))
                    break
                except ValueError:
                    print("Please enter a number.")
            if order_amount > max_amount:
                print(f"-------\nMax order amount is {max_amount}.\n-------")
                max_order = input(f"Order {max_amount} of '{item}'?(y/n) ")
                if max_order:
                    print(f"{max_amount} of '{item}' have been ordered.")
            else:
                print(f"{order_amount} of '{item}' have been ordered.")

# Else, if they pick 3
    elif opt == "3":
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
