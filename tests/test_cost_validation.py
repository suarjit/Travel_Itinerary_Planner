
import pytest

from src.workflow.travel_graph import validate_travel_inputs

def valid_input():
    return {
        "destination": "Darjeeling, India",
        "days": 3,
        "daily_hotel_cost": 1500,
        "daily_food_cost": 800,
        "transport_cost": 2000,
        "attraction_cost": 1000,
        "total_budget": 12000,
        "transport_mode": "car"
    }

@pytest.mark.parametrize(
    "field",
    [
        "daily_hotel_cost",
        "daily_food_cost",
        "transport_cost",
        "attraction_cost",
        "total_budget"
    ]
)
def test_negative_cost_fields(field):
    data = valid_input()
    data[field] = -100

    errors = validate_travel_inputs(data)

    assert f"{field} cannot be negative." in errors

@pytest.mark.parametrize(
    "field",
    [
        "daily_hotel_cost",
        "daily_food_cost",
        "transport_cost",
        "attraction_cost",
        "total_budget"
    ]
)
def test_invalid_cost_types(field):
    data = valid_input()
    data[field] = "invalid"

    errors = validate_travel_inputs(data)

    assert f"{field} must be a valid number." in errors

def test_zero_costs_are_accepted():
    data = valid_input()

    for field in [
        "daily_hotel_cost",
        "daily_food_cost",
        "transport_cost",
        "attraction_cost",
        "total_budget"
    ]:
        data[field] = 0

    assert validate_travel_inputs(data) == []