from src.tools import Tool, ToolRegistry


def calculate_total(price: float, quantity: int) -> float:
    if price < 0:
        raise ValueError("Price cannot be negative.")

    if quantity < 0:
        raise ValueError("Quantity cannot be negative.")

    return price * quantity


def build_default_registry() -> ToolRegistry:
    registry = ToolRegistry()

    registry.register(
        Tool(
            name="calculate_total",
            description="Calculate a total price from unit price and quantity.",
            function=calculate_total,
        )
    )

    return registry
