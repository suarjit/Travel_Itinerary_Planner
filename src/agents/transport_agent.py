

from src.tools.transport_tool import estimate_transport
from src.utils.logger import WorkflowLogger

class TransportAgent:

    def __init__(self):
        self.name = "Transport Agent"
        self.logger = WorkflowLogger()

    def run(
        self,
        origin_lat,
        origin_lon,
        daily_itinerary,
        transport_mode="car"
    ):

        print(f"{self.name} started...")
        print("Calculating day-wise transport estimates...")

        inputs = {
            "origin_lat": origin_lat,
            "origin_lon": origin_lon,
            "total_days": len(daily_itinerary),
            "transport_mode": transport_mode
        }

        self.logger.log_agent_start(self.name, inputs)

        try:

            if not isinstance(daily_itinerary, list) or not daily_itinerary:
                raise ValueError("Daily itinerary must be a non-empty list.")

            daily_transport = []
            total_distance = 0
            total_travel_time = 0

            for day in daily_itinerary:

                activities = day.get("activities", [])

                if not activities:
                    daily_transport.append({
                        "day": day["day"],
                        "journeys": [],
                        "total_distance_km": 0,
                        "total_travel_time_minutes": 0
                    })
                    continue

                journeys = []
                day_distance = 0
                day_travel_time = 0

                current_lat = origin_lat
                current_lon = origin_lon

                for attraction in activities:

                    result = estimate_transport(
                        current_lat,
                        current_lon,
                        attraction["latitude"],
                        attraction["longitude"],
                        transport_mode
                    )

                    journeys.append({
                        "destination": attraction.get("name", "Unnamed attraction"),
                        "distance_km": result["distance_km"],
                        "estimated_travel_time_minutes":
                            result["estimated_travel_time_minutes"]
                    })

                    day_distance += result["distance_km"]
                    day_travel_time += result["estimated_travel_time_minutes"]

                    current_lat = attraction["latitude"]
                    current_lon = attraction["longitude"]

                daily_transport.append({
                    "day": day["day"],
                    "journeys": journeys,
                    "total_distance_km": round(day_distance, 2),
                    "total_travel_time_minutes": round(day_travel_time, 2)
                })

                total_distance += day_distance
                total_travel_time += day_travel_time

            final_result = {
                "success": True,
                "daily_transport": daily_transport,
                "total_distance_km": round(total_distance, 2),
                "total_travel_time_minutes": round(total_travel_time, 2),
                "transport_mode": transport_mode,
                "note": "Approximate straight-line estimates, not verified road routes."
            }

            self.logger.log_tool_call(
                "estimate_daily_transport",
                inputs,
                final_result
            )

            self.logger.log_agent_end(self.name, "success")

            return {
                "agent": self.name,
                "status": "success",
                **final_result
            }

        except Exception as error:

            self.logger.log_error(self.name, error)
            self.logger.log_agent_end(self.name, "failed")

            return {
                "agent": self.name,
                "status": "failed",
                "error": str(error)
            }

if __name__ == "__main__":

    print("Transport Agent supports day-wise itinerary calculations.")
