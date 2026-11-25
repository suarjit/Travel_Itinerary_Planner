
from src.workflow.travel_graph import run_travel_workflow

if __name__ == "__main__":

    result = run_travel_workflow(
        destination="Darjeeling, India",
        days=3,
        daily_hotel_cost=1500,
        daily_food_cost=800,
        transport_cost=2000,
        attraction_cost=1000,
        total_budget=12000,
        transport_mode="car"
    )

    print("\n========== FINAL TRAVEL PLAN ==========")

    print("\nFinal Status:")
    print(result.get("status"))

    print("\nDay-wise Itinerary:")
    itinerary = result.get("itinerary_info", {})

    for day in itinerary.get("daily_itinerary", []):
        print(f"\nDay {day['day']}")

        for activity in day["activities"]:
            print(f"- {activity.get('name', 'Unnamed attraction')}")

    print("\nTransport Information:")

    transport = result.get("transport_info", {})

    if transport.get("status") == "success":

        for day in transport.get("daily_transport", []):

            print(f"\nDay {day['day']}")
            print(f"Total Distance: {day['total_distance_km']} km")
            print(
                f"Total Travel Time: "
                f"{day['total_travel_time_minutes']} minutes"
            )

            for journey in day["journeys"]:
                print(
                    f"- {journey['destination']}: "
                    f"{journey['distance_km']} km, "
                    f"{journey['estimated_travel_time_minutes']} minutes"
                )

        print("\nOverall Transport Summary:")
        print(f"Total Distance: {transport['total_distance_km']} km")
        print(
            f"Total Travel Time: "
            f"{transport['total_travel_time_minutes']} minutes"
        )

    else:
        print(transport)

        

    print("\nBudget Information:")
    print(result.get("budget_info"))

    print("\nErrors:")
    print(result.get("errors", []))