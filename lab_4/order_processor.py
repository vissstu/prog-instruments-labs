class OrderProcessor:
    def __init__(self):
        self.data = []

    def process(self, items, customer_type, is_weekend, coupon_code=None):
        # Calculate subtotal
        subtotal = 0
        for i in items:
            subtotal += i['price'] * i['quantity']

        # Apply discounts based on customer type
        discount = 0
        if customer_type == "vip":
            if subtotal > 1000:
                discount = subtotal * 0.2
            elif subtotal > 500:
                discount = subtotal * 0.1
            else:
                discount = subtotal * 0.05
        elif customer_type == "regular":
            if subtotal > 500:
                discount = subtotal * 0.05

        # Weekend surcharge
        if is_weekend:
            subtotal = subtotal * 1.1

        # Apply coupon if exists
        if coupon_code:
            if coupon_code == "SAVE10":
                discount += subtotal * 0.1
            elif coupon_code == "SAVE20":
                discount += subtotal * 0.2
            elif coupon_code == "FREESHIP":
                # Free shipping logic (flat $10 discount)
                discount += 10

        # Calculate tax
        tax = (subtotal - discount) * 0.08

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
        if len(items) > 5:
            total = total * 0.95  # 5% discount for more than 5 items

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