
from unittest.mock import patch

from src.agents.destination_agent import DestinationResearchAgent

def test_destination_agent_success():

    mock_result = {
        
        "success": True,
        "destination": "Darjeeling, India",
        "attractions": [
            {"name": "Batasia Loop"},
            {"name": "Tiger Hill"}
        ],
        "total_attractions": 2,
        "data_source": "OpenStreetMap Live API",
        "cached": False
    }

    with patch(
        "src.agents.destination_agent.research_destination",
        return_value=mock_result
    ):

        agent = DestinationResearchAgent()
        result = agent.run("Darjeeling, India")

    assert result["status"] == "success"
    assert result["destination"] == "Darjeeling, India"
    assert result["total_attractions"] == 2
    assert result["data_source"] == "OpenStreetMap Live API"
    assert result["cached"] is False

def test_destination_agent_failure():

    with patch(
        "src.agents.destination_agent.research_destination",
        side_effect=Exception("API connection failed")
    ):

        agent = DestinationResearchAgent()
        result = agent.run("Darjeeling, India")

    assert result["status"] == "failed"
    assert "API connection failed" in result["error"]