import unittest

from classes import Item, Warehouse, User, Employee

class Test(unittest.TestCase):
    def test_Item(self):
        data = {
            "state": "High quality",
            "category": "USB hub",
            "warehouse": 1,
            "date_of_stock": "2020-08-01 02:58:45",
        }
        item = Item(**data)
        reality = [
            item.state,
            item.category,
            item.date_of_stock,
            item.warehouse,
            str(item)
        ]
        expectation = [
            "High quality",
            "USB hub",
            "2020-08-01 02:58:45",
            1,
            "High quality USB hub"
        ]
        self.assertEqual(reality, expectation)

    def test_Warehouse(self):
        warehouse = Warehouse(1)
        data1 = {
            "state": "High quality",
            "category": "USB hub",
            "warehouse": 1,
            "date_of_stock": "2020-08-01 02:58:45"
        }
        data2 = {
            "state": "Exceptional",
            "category": "iOS charger",
            "warehouse": 1,
            "date_of_stock": "2021-03-08 13:22:31"
        }
        data3 = {
            "state": "Elegant",
            "category": "GPS",
            "warehouse": 1,
            "date_of_stock": "2020-09-08 01:32:03"
        }
        item1 = Item(**data1)
        item2 = Item(**data2)
        item3 = Item(**data3)
        warehouse.add_item(item1)
        warehouse.add_item(item2)
        warehouse.add_item(item3)
        reality = [
            str(warehouse),
            warehouse.occupancy(),
            warehouse.get_items(),
            warehouse.search('elegant gps')
        ]
        expectation = [
            'Warehouse 1',
            3,
            [
                item1,
                item2,
                item3
            ],
            [item3]
        ]
        self.assertEqual(reality, expectation)

    def test_User_Employee(self):
        user0 = User('Luca')
        user1 = Employee('Jorge', 'testpw', [])
        user2 = Employee('Carlos', 'test2pw', [user1])
        data = {
            "state": "High quality",
            "category": "USB hub",
            "warehouse": 1,
            "date_of_stock": "2020-08-01 02:58:45"
        }
        item = Item(**data)
        reality = [
            user0.authenticate('random_things'),
            user1.authenticate('testpw'),
            user2.authenticate('testpw'),
            user0.is_named('Luca'),
            user1.is_named('Luca'),
            user2.head_of,
            user1.order(item, 3),
        ]
        expectation = [
            False,
            True,
            False,
            True,
            False,
            [user1],
            None,
        ]
        self.assertEqual(reality, expectation)
