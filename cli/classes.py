from datetime import datetime as dt


class Item:
    def __init__(self, **kwargs):
        self.state = kwargs['state']
        self.category = kwargs['category']
        self.date_of_stock = kwargs['date_of_stock']
        self.warehouse = kwargs['warehouse']

    def __str__(self):
        return f"{self.state} {self.category}"


class Warehouse:
    def __init__(self, id: int):
        self.stock = list()
        self.id = id

    def __iter__(self):
        return iter(self.stock)

    def __str__(self):
        return f'Warehouse {self.id}'

    def occupancy(self):
        return len(self.stock)

    def get_items(self):
        return self.stock

    def add_item(self, item: Item):
        self.stock.append(item)

    def search(self, lookup: str):
        return [x for x in self.stock if str(x).lower() == lookup.lower()]


class User:
    def __init__(self, user_name: str):
        self._name = user_name if user_name else 'Anonymous'
        self.is_authenticated = False

    def authenticate(self, password: str):
        return False

    def is_named(self, name: str):
        return name == self._name

    def greet(self):
        print(
            f"Hello, {self._name}!",
            "Welcome to our Warehouse Database.",
            "If you don't find what you are looking for,",
            "please ask one of our staff members to assist you.",
            sep="\n"
        )

    def update_log(self, update):
        return False

    def bye(self):
        print(f"Good bye, {self._name}.")


class Employee(User):

    def __init__(self, user_name: str, password: str, head_of: list = []):
        super().__init__(user_name)
        self.__password = password
        self.head_of = head_of
        self.log = list()

    def authenticate(self, password: str):
        self.is_authenticated = password == self.__password
        return self.is_authenticated

    def order(self, item: Item, amount: int):
        print(f"Ordered: {amount} of {item}.")

    def greet(self):
        print(
            f"Hello, {self._name}!",
            "If you experience a problem with the system,",
            "please contact technical support.",
            sep="\n"
        )

    def update_log(self, update):
        self.log.append(update)

    def bye(self):
        super().bye()
        if self.is_authenticated:
            print("Actions taken:")
            for entry, action in enumerate(self.log, start=1):
                print(f"{entry}. {action}")
