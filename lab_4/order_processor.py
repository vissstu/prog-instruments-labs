from constants import Constants
from models import *


class OrderProcessor:
    def __init__(self):
        self.data = []

    def _calculate_customer_discount(self, customer_type, subtotal):
        """Calculate discount based on customer type and order amount."""
        if customer_type == "vip":
            if subtotal > Constants.VIP_LARGE_THRESHOLD:
                return subtotal * Constants.VIP_DISCOUNT_LARGE
            elif subtotal > Constants.VIP_MEDIUM_THRESHOLD:
                return subtotal * Constants.VIP_DISCOUNT_MEDIUM
            else:
                return subtotal * Constants.VIP_DISCOUNT_SMALL
        elif customer_type == "regular":
            if subtotal > Constants.REGULAR_DISCOUNT_THRESHOLD:
                return subtotal * Constants.REGULAR_DISCOUNT
        return 0.0

    def process(self, items, customer_type, is_weekend, coupon_code=None):
        # Создаем объекты

        customer = Customer(customer_type)
        order = Order(items, customer, coupon_code, is_weekend)

        # Теперь работаем с объектами
        subtotal = order.subtotal
        customer_type = order.customer.type

        # Apply discounts based on customer type
        customer_discount = self._calculate_customer_discount(customer_type, subtotal)
        discount = customer_discount

        # Weekend surcharge
        if is_weekend:
            subtotal = subtotal * (1 + Constants.WEEKEND_SURCHARGE_RATE)

        # Apply coupon if exists
        if order.coupon_code:
            if order.coupon_code == "SAVE10":
                discount += subtotal * Constants.COUPON_SAVE10
            elif order.coupon_code == "SAVE20":
                discount += subtotal * Constants.COUPON_SAVE20
            elif order.coupon_code == "FREESHIP":
                # Free shipping logic (flat $10 discount)
                discount += Constants.COUPON_FREESHIP

        # Calculate tax
        tax = (subtotal - discount) * Constants.TAX_RATE

        # Calculate final total
        total = subtotal - discount + tax

        # Log the transaction
        self.data.append({
            "sub": subtotal,
            "dis": discount,
            "tax": tax,
            "tot": total,
            "items": len(items)
        })

        # Check if we need to apply special offer
        if order.item_count > Constants.BULK_ITEM_THRESHOLD:
            total = total * (1 - Constants.BULK_DISCOUNT)  # 5% discount for more than 5 items

        return total

    def get_report(self):
        total_sales = 0
        total_discounts = 0
        for d in self.data:
            total_sales += d['tot']
            total_discounts += d['dis']

        avg = total_sales / len(self.data) if self.data else 0

        return f"Sales: {total_sales}, Discounts: {total_discounts}, Avg: {avg}"

    def find_big_orders(self, threshold):
        result = []
        for d in self.data:
            if d['tot'] > threshold:
                result.append(d)
        return result


