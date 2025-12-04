class OrderItem:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    @property
    def total_price(self):
        return self.price * self.quantity


class Customer:
    def __init__(self, customer_type):
        self.type = customer_type
        self.is_vip = customer_type == "vip"
        self.is_regular = customer_type == "regular"


class Order:
    def __init__(self, items, customer, coupon_code=None, is_weekend=False):
        self.items = items
        self.customer = customer
        self.coupon_code = coupon_code
        self.is_weekend = is_weekend
        self.subtotal = self._calculate_subtotal()

    def _calculate_subtotal(self):
        return sum(item.total_price for item in self.items)

    @property
    def item_count(self):
        return len(self.items)

