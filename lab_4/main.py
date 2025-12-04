from order_processor import OrderProcessor


def main():
    processor = OrderProcessor()

    # Sample order
    items = [
        {"name": "Laptop", "price": 999.99, "quantity": 1},
        {"name": "Mouse", "price": 29.99, "quantity": 2},
        {"name": "Keyboard", "price": 79.99, "quantity": 1},
        {"name": "Monitor", "price": 299.99, "quantity": 1},
    ]

    # Process order with various parameters
    total = processor.process(
        items=items,
        customer_type="vip",
        is_weekend=True,
        coupon_code="SAVE10"
    )

    print(f"Total: ${total:.2f}")
    print(processor.get_report())

    # Find big orders
    big_orders = processor.find_big_orders(1000)
    print(f"Big orders: {len(big_orders)}")


if __name__ == "__main__":
    main()