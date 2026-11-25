
from unittest.mock import patch

from src.agents.transport_agent import TransportAgent

def test_transport_agent_single_day():

    itinerary = [
        {
            "day": 1,
            "activities": [
                {
                    "name": "Attraction A",
                    "latitude": 27.05,
                    "longitude": 88.26
                },
                {
                    "name": "Attraction B",
                    "latitude": 27.06,
                    "longitude": 88.27
                }
            ]
        }
    ]

    mock_results = [
        {
            "success": True,
            "distance_km": 2.0,
            "estimated_travel_time_minutes": 5.0
        },
        {
            "success": True,
            "distance_km": 3.0,
            "estimated_travel_time_minutes": 8.0
        }
    ]

    with patch(
        "src.agents.transport_agent.estimate_transport",
        side_effect=mock_results
    ):

        agent = TransportAgent()

        result = agent.run(
            origin_lat=27.04,
            origin_lon=88.25,
            daily_itinerary=itinerary,
            transport_mode="car"
        )

    assert result["status"] == "success"
    assert result["total_distance_km"] == 5.0
    assert result["total_travel_time_minutes"] == 13.0
    assert len(result["daily_transport"]) == 1
    assert len(result["daily_transport"][0]["journeys"]) == 2

def test_transport_agent_multiple_days():

    itinerary = [
        {
            "day": 1,
            "activities": [
                {
                    "name": "Attraction A",
                    "latitude": 27.05,
                    "longitude": 88.26
                }
            ]
        },
        {
            "day": 2,
            "activities": [
                {
                    "name": "Attraction B",
                    "latitude": 27.06,
                    "longitude": 88.27
                }
            ]
        }
    ]

    mock_results = [
        {
            "success": True,
            "distance_km": 2.0,
            "estimated_travel_time_minutes": 5.0
        },
        {
            "success": True,
            "distance_km": 3.0,
            "estimated_travel_time_minutes": 8.0
        }
    ]

    with patch(
        "src.agents.transport_agent.estimate_transport",
        side_effect=mock_results
    ):

        agent = TransportAgent()

        result = agent.run(
            origin_lat=27.04,
            origin_lon=88.25,
            daily_itinerary=itinerary
        )

    assert result["status"] == "success"
    assert len(result["daily_transport"]) == 2
    assert result["total_distance_km"] == 5.0
    assert result["total_travel_time_minutes"] == 13.0

def test_transport_agent_empty_itinerary():

    agent = TransportAgent()

    result = agent.run(
        origin_lat=27.04,
        origin_lon=88.25,
        daily_itinerary=[]
    )

    assert result["status"] == "failed"
    assert "non-empty list" in result["error"]

def test_transport_agent_empty_day():

    itinerary = [
        {
            "day": 1,
            "activities": []
        }
    ]

    agent = TransportAgent()

    result = agent.run(
        origin_lat=27.04,
        origin_lon=88.25,
        daily_itinerary=itinerary
    )

    assert result["status"] == "success"
    assert result["daily_transport"][0]["total_distance_km"] == 0
    assert result["daily_transport"][0]["total_travel_time_minutes"] == 0