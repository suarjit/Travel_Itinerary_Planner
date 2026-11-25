
from src.utils.logger import WorkflowLogger

class ItineraryPlanningAgent:

    def __init__(self):
        self.name = "Itinerary Planning Agent"
        self.logger = WorkflowLogger()

    def run(self, destination, days, attractions):

        print(f"{self.name} started...")
        print(f"Planning a {days}-day trip to {destination}")

        try:

            if not isinstance(days, int) or isinstance(days, bool) or days <= 0:
                raise ValueError(
                    "Trip duration must be a positive whole number."
                )

            if not isinstance(attractions, list) or not attractions:
                raise ValueError(
                    "Attractions must be a non-empty list."
                )

            self.logger.log_agent_start(
                self.name,
                {
                    "destination": destination,
                    "days": days,
                    "total_attractions": len(attractions)
                }
            )

            daily_itinerary = []

            total_attractions = len(attractions)
            
            base_count = total_attractions // days
            remainder = total_attractions % days

            attraction_index = 0

            for day in range(1, days + 1):

                daily_count = base_count

                if day <= remainder:
                    daily_count += 1

                daily_activities = attractions[
                    attraction_index:attraction_index + daily_count
                ]

                daily_itinerary.append({
                    "day": day,
                    "activities": daily_activities
                })

                attraction_index += daily_count

            result = {
                "destination": destination,
                "total_days": days,
                "daily_itinerary": daily_itinerary,
                "total_attractions": total_attractions
            }

            self.logger.log_agent_end(self.name, "success")

            return {
                "agent": self.name,
                "status": "success",
                **result
            }

        except Exception as error:

            self.logger.log_error(self.name, error)
            self.logger.log_agent_end(self.name, "failed")

            return {
                "agent": self.name,
                "status": "failed",
                "error": str(error)
            }