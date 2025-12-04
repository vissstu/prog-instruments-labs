import unittest
from order_processor import OrderProcessor


class TestOrderProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = OrderProcessor()
        self.items = [
            {"price": 100, "quantity": 2},
            {"price": 50, "quantity": 1},
        ]

    def test_regular_customer(self):
        total = self.processor.process(
            items=self.items,
            customer_type="regular",
            is_weekend=False
        )
        # Subtotal: 250, discount: 0, tax: 20, total: 270
        self.assertAlmostEqual(total, 270, delta=0.1)

    def test_vip_customer_with_discount(self):
        total = self.processor.process(
            items=self.items,
            customer_type="vip",
            is_weekend=False
        )
        # Subtotal: 250, discount: 12.5 (5% of 250), tax: 19, total: ~256.5
        self.assertAlmostEqual(total, 256.5, delta=0.1)

    def test_with_coupon(self):
        total = self.processor.process(
            items=self.items,
            customer_type="regular",
            is_weekend=False,
            coupon_code="SAVE10"
        )
        # Subtotal: 250, discount: 25 (10%), tax: 18, total: 243
        self.assertAlmostEqual(total, 243, delta=0.1)


if __name__ == "__main__":
    unittest.main()