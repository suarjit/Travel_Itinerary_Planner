
def calculate_travel_budget(
    days,
    daily_hotel_cost,
    daily_food_cost,
    transport_cost,
    attraction_cost,
    total_budget
):
    """
    Calculate estimated travel expenses.
    """

    if days <= 0 or total_budget < 0:
        raise ValueError("Days must be positive and budget cannot be negative.")

    costs = [
        daily_hotel_cost,
        daily_food_cost,
        transport_cost,
        attraction_cost
    ]

    if any(cost < 0 for cost in costs):
        raise ValueError("Expenses cannot be negative.")

    accommodation = days * daily_hotel_cost
    food = days * daily_food_cost
    total_transport = transport_cost
    total_attractions = attraction_cost

    total_expenses = (
        accommodation
        + food
        + total_transport
        + total_attractions
    )

    remaining_budget = total_budget - total_expenses

    return {
        "success": True,
        "trip_duration_days": days,
        "budget": total_budget,
        "expenses": {
            "accommodation": accommodation,
            "food": food,
            "transport": total_transport,
            "attractions": total_attractions
        },
        "total_expenses": total_expenses,
        "remaining_budget": remaining_budget,
        "within_budget": total_expenses <= total_budget
    }