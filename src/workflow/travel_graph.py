
import math
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

from src.agents.destination_agent import DestinationResearchAgent
from src.agents.transport_agent import TransportAgent
from src.agents.budget_agent import BudgetPlanningAgent
from src.agents.itinerary_agent import ItineraryPlanningAgent
from src.utils.logger import WorkflowLogger

class TravelState(TypedDict, total=False):
    destination: str
    days: int
    daily_hotel_cost: float
    daily_food_cost: float
    transport_cost: float
    attraction_cost: float
    total_budget: float
    transport_mode: str

    destination_info: dict
    selected_attraction: dict
    itinerary_info: dict
    transport_info: dict
    budget_info: dict

    logs: list
    errors: list
    status: str

def destination_node(state: TravelState):
    print("\n--- Destination Research Node ---")

    logger = WorkflowLogger()

    logger.log_event("state_transition", {
        "from": "validation_node",
        "to": "destination_node",
        "status": "running"
    })

    agent = DestinationResearchAgent()
    result = agent.run(state["destination"])

    log = {
    "node": "destination_node",
    "agent": result["agent"],
    "status": result["status"],
    "data_source": result.get("data_source", "Unknown"),
    "cached": result.get("cached", False),
    "total_attractions": result.get("total_attractions", 0)
}

    if result["status"] != "success":
        error = result.get("error", result.get("message", "Destination research failed."))

        logger.log_event("state_transition", {
            "from": "destination_node",
            "to": "END",
            "status": "failed"
        })

        return {
            "destination_info": result,
            "logs": state.get("logs", []) + [log],
            "errors": state.get("errors", []) + [error],
            "status": "failed"
        }

    attractions = result["attractions"]

    if not attractions:
        logger.log_event("state_transition", {
            "from": "destination_node",
            "to": "END",
            "status": "failed"
        })

        return {
            "destination_info": result,
            "logs": state.get("logs", []) + [log],
            "errors": state.get("errors", []) + ["No attractions found."],
            "status": "failed"
        }

    logger.log_event("state_transition", {
        "from": "destination_node",
        "to": "itinerary",
        "status": "success"
    })

    return {
        "destination_info": result,
        "selected_attraction": attractions[0],
        "logs": state.get("logs", []) + [log],
        "status": "success"
    }

def itinerary_node(state: TravelState):

    print("\n--- Itinerary Planning Node ---")

    logger = WorkflowLogger()

    agent = ItineraryPlanningAgent()

    destination = state["destination_info"]["destination"]["display_name"]
    attractions = state["destination_info"]["attractions"]

    result = agent.run(
        destination=destination,
        days=state.get("days", 3),
        attractions=attractions
    )

    log = {
        "node": "itinerary_node",
        "agent": result["agent"],
        "status": result["status"],
        "total_days": result.get("total_days", 0),
        "total_attractions": result.get("total_attractions", 0)
    }

    if result["status"] != "success":

        error = result.get("error", "Itinerary planning failed.")

        logger.log_event("state_transition", {
            "from": "itinerary_node",
            "to": "END",
            "status": "failed"
        })

        return {
            "itinerary_info": result,
            "logs": state.get("logs", []) + [log],
            "errors": state.get("errors", []) + [error],
            "status": "failed"
        }

    logger.log_event("state_transition", {
        "from": "itinerary_node",
        "to": "transport",
        "status": "success"
    })

    return {
        "itinerary_info": result,
        "logs": state.get("logs", []) + [log],
        "status": "success"
    }

def transport_node(state: TravelState):

    print("\n--- Transport Node ---")

    logger = WorkflowLogger()

    destination = state["destination_info"]["destination"]
    itinerary = state["itinerary_info"]["daily_itinerary"]

    agent = TransportAgent()

    result = agent.run(
        origin_lat=destination["latitude"],
        origin_lon=destination["longitude"],
        daily_itinerary=itinerary,
        transport_mode=state.get("transport_mode", "car")
    )

    log = {
        "node": "transport_node",
        "agent": result["agent"],
        "status": result["status"]
    }

    if result["status"] != "success":

        error = result.get("error", "Transport estimation failed.")

        logger.log_event("state_transition", {
            "from": "transport_node",
            "to": "END",
            "status": "failed"
        })

        return {
            "transport_info": result,
            "logs": state.get("logs", []) + [log],
            "errors": state.get("errors", []) + [error],
            "status": "failed"
        }

    logger.log_event("state_transition", {
        "from": "transport_node",
        "to": "budget_node",
        "status": "success"
    })

    return {
        "transport_info": result,
        "logs": state.get("logs", []) + [log],
        "status": "success"
    }

def budget_node(state: TravelState):
    print("\n--- Budget Planning Node ---")

    logger = WorkflowLogger()

    agent = BudgetPlanningAgent()

    result = agent.run(
        days=state.get("days", 3),
        daily_hotel_cost=state.get("daily_hotel_cost", 1500),
        daily_food_cost=state.get("daily_food_cost", 800),
        transport_cost=state.get("transport_cost", 2000),
        attraction_cost=state.get("attraction_cost", 1000),
        total_budget=state.get("total_budget", 12000)
    )

    log = {
        "node": "budget_node",
        "agent": result["agent"],
        "status": result["status"]
    }

    if result["status"] != "success":
        error = result.get("error", "Budget planning failed.")

        logger.log_event("state_transition", {
            "from": "budget_node",
            "to": "END",
            "status": "failed"
        })

        return {
            "budget_info": result,
            "logs": state.get("logs", []) + [log],
            "errors": state.get("errors", []) + [error],
            "status": "failed"
        }

    logger.log_event("state_transition", {
        "from": "budget_node",
        "to": "END",
        "status": "success"
    })

    return {
        "budget_info": result,
        "logs": state.get("logs", []) + [log],
        "status": "success"
    }

def check_status(state: TravelState):
    if state.get("status") == "success":
        return "continue"

    return "stop"


def validate_travel_inputs(state: TravelState):

    errors = []

    # Validate destination
    destination = state.get("destination")

    if not isinstance(destination, str) or not destination.strip():
        errors.append("Destination cannot be empty.")

    # Validate trip duration
    days = state.get("days", 3)

    if isinstance(days, bool) or not isinstance(days, int):
        errors.append("Trip duration must be a whole number.")
    elif days <= 0:
        errors.append("Trip duration must be greater than zero.")

    # Validate budget and cost fields
    cost_fields = [
        "daily_hotel_cost",
        "daily_food_cost",
        "transport_cost",
        "attraction_cost",
        "total_budget"
    ]

    for field in cost_fields:

        value = state.get(field, 0)

        if isinstance(value, bool) or not isinstance(value, (int, float)):
            errors.append(f"{field} must be a valid number.")

        elif not math.isfinite(value):
            errors.append(f"{field} must be a finite number.")

        elif value < 0:
            errors.append(f"{field} cannot be negative.")

    # Validate transport mode
    allowed_modes = ["walking", "car", "bus", "train"]

    transport_mode = state.get("transport_mode", "car")

    if not isinstance(transport_mode, str):
        errors.append("Transport mode must be text.")

    elif transport_mode.strip().lower() not in allowed_modes:
        errors.append("Unsupported transport mode.")

    return errors
def validation_node(state: TravelState):

    print("\n--- Input Validation Node ---")

    logger = WorkflowLogger()

    logger.log_event("state_transition", {
        "from": "START",
        "to": "validation_node",
        "status": "running"
    })

    errors = validate_travel_inputs(state)

    if errors:
        print("Input validation failed:", errors)

        logger.log_event("state_transition", {
            "from": "validation_node",
            "to": "END",
            "status": "failed"
        })

        return {
            "errors": state.get("errors", []) + errors,
            "status": "failed"
        }

    print("All travel inputs are valid.")

    logger.log_event("state_transition", {
        "from": "validation_node",
        "to": "destination_node",
        "status": "success"
    })

    return {
        "status": "success"
    }


def build_travel_graph():

    workflow = StateGraph(TravelState)

    workflow.add_node("validation", validation_node)
    workflow.add_node("destination", destination_node)
    workflow.add_node("itinerary", itinerary_node)
    workflow.add_node("transport", transport_node)
    workflow.add_node("budget", budget_node)

    workflow.add_edge(START, "validation")

    workflow.add_conditional_edges(
        "validation",
        check_status,
        {
            "continue": "destination",
            "stop": END
        }
    )

    workflow.add_conditional_edges(
        "destination",
        check_status,
        {
            "continue": "itinerary",
            "stop": END
        }
    )

    workflow.add_conditional_edges(
        "itinerary",
        check_status,
        {
            "continue": "transport",
            "stop": END
        }
    )

    workflow.add_conditional_edges(
        "transport",
        check_status,
        {
            "continue": "budget",
            "stop": END
        }
    )

    workflow.add_edge("budget", END)

    return workflow.compile()

def run_travel_workflow(
    destination,
    days=3,
    daily_hotel_cost=1500,
    daily_food_cost=800,
    transport_cost=2000,
    attraction_cost=1000,
    total_budget=12000,
    transport_mode="car"
):

    graph = build_travel_graph()

    initial_state = {
        "destination": destination,
        "days": days,
        "daily_hotel_cost": daily_hotel_cost,
        "daily_food_cost": daily_food_cost,
        "transport_cost": transport_cost,
        "attraction_cost": attraction_cost,
        "total_budget": total_budget,
        "transport_mode": transport_mode,
        "logs": [],
        "errors": [],
        "status": "running"
    }

    return graph.invoke(initial_state)