from constants import Constants
from models import *


class OrderProcessor:
    def __init__(self):
        self.order_history = []

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

    def _calculate_coupon_discount(self, coupon_code, subtotal):
        """Calculate additional discount from coupon code."""
        if not coupon_code:
            return 0.0

        if coupon_code == "SAVE10":
            return subtotal * Constants.COUPON_SAVE10
        elif coupon_code == "SAVE20":
            return subtotal * Constants.COUPON_SAVE20
        elif coupon_code == "FREESHIP":
            return Constants.COUPON_FREESHIP

        return 0.0

    def calculate_order_total(self, items, customer_type, is_weekend, coupon_code=None):
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
        coupon_discount = self._calculate_coupon_discount(coupon_code, subtotal)
        discount += coupon_discount

        # Calculate tax
        tax = (subtotal - discount) * Constants.TAX_RATE

        # Calculate final total
        total = subtotal - discount + tax

        # Log the transaction
        self.order_history.append({
            "subtotal": subtotal,
            "discount": discount,
            "tax": tax,
            "total": total,
            "item_count": len(items)
        })

        # Check if we need to apply special offer
        if order.item_count > Constants.BULK_ITEM_THRESHOLD:
            total = total * (1 - Constants.BULK_DISCOUNT)  # 5% discount for more than 5 items

        return total

    def get_report(self):
        total_sales = 0
        total_discounts = 0
        for d in self.order_history:
            total_sales += d['tot']
            total_discounts += d['dis']

        avg = total_sales / len(self.order_history) if self.order_history else 0

        return f"Sales: {total_sales}, Discounts: {total_discounts}, Avg: {avg}"

    def find_big_orders(self, threshold):
        result = []
        for d in self.order_history:
            if d['tot'] > threshold:
                result.append(d)
        return result


