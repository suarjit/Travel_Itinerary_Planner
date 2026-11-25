
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

def test_valid_input():
    assert validate_travel_inputs(valid_input()) == []

@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_non_finite_hotel_cost(value):
    data = valid_input()
    data["daily_hotel_cost"] = value

    errors = validate_travel_inputs(data)

    assert "daily_hotel_cost must be a finite number." in errors

def test_negative_hotel_cost():
    data = valid_input()
    data["daily_hotel_cost"] = -100

    errors = validate_travel_inputs(data)

    assert "daily_hotel_cost cannot be negative." in errors

def test_invalid_trip_duration():
    data = valid_input()
    data["days"] = -2

    errors = validate_travel_inputs(data)

    assert "Trip duration must be greater than zero." in errors

def test_invalid_transport_mode():
    data = valid_input()
    data["transport_mode"] = "airplane"

    errors = validate_travel_inputs(data)

    assert "Unsupported transport mode." in errors

def test_empty_destination():
    data = valid_input()
    data["destination"] = "   "

    errors = validate_travel_inputs(data)

    assert "Destination cannot be empty." in errors