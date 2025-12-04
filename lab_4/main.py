from order_processor import *


def main():
    processor = OrderProcessor()

    # Sample order
    items = [
        OrderItem("Laptop", 999.99, 1),
        OrderItem("Mouse", 29.99, 2),
        OrderItem("Keyboard", 79.99, 1),
        OrderItem("Monitor", 299.99, 1),
    ]

    # Process order with various parameters
    total = processor.calculate_order_total(
        items=items,  # Теперь это список OrderItem, не словарей
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