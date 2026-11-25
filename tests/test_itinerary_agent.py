
from src.agents.itinerary_agent import ItineraryPlanningAgent

def test_itinerary_generation():

    agent = ItineraryPlanningAgent()

    attractions = [
        {"name": "Tiger Hill"},
        {"name": "Batasia Loop"},
        {"name": "Rock Garden"},
        {"name": "Peace Pagoda"},
        {"name": "Himalayan Mountaineering Institute"}
    ]

    result = agent.run(
        destination="Darjeeling, India",
        days=3,
        attractions=attractions
    )

    assert result["status"] == "success"
    assert result["total_days"] == 3
    assert result["total_attractions"] == 5
    assert len(result["daily_itinerary"]) == 3

def test_attraction_distribution():

    agent = ItineraryPlanningAgent()

    attractions = [
        {"name": "Tiger Hill"},
        {"name": "Batasia Loop"},
        {"name": "Rock Garden"},
        {"name": "Peace Pagoda"},
        {"name": "HMI"}
    ]

    result = agent.run(
        destination="Darjeeling, India",
        days=3,
        attractions=attractions
    )

    daily_itinerary = result["daily_itinerary"]

    assert len(daily_itinerary[0]["activities"]) == 2
    assert len(daily_itinerary[1]["activities"]) == 2
    assert len(daily_itinerary[2]["activities"]) == 1

def test_invalid_trip_duration():

    agent = ItineraryPlanningAgent()

    result = agent.run(
        destination="Darjeeling, India",
        days=0,
        attractions=[{"name": "Tiger Hill"}]
    )

    assert result["status"] == "failed"

def test_empty_attractions():

    agent = ItineraryPlanningAgent()

    result = agent.run(
        destination="Darjeeling, India",
        days=3,
        attractions=[]
    )

    assert result["status"] == "failed"