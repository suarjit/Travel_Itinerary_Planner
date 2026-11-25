from src.tools.budget_tool import calculate_travel_budget
from src.utils.logger import WorkflowLogger

class BudgetPlanningAgent:

    def __init__(self):
        self.name = "Budget Planning Agent"
        self.logger = WorkflowLogger()

    def run(
        self,
        days,
        daily_hotel_cost,
        daily_food_cost,
        transport_cost,
        attraction_cost,
        total_budget
    ):

        print(f"{self.name} started...")
        print("Calculating travel expenses...")

        inputs = {
            "days": days,
            "daily_hotel_cost": daily_hotel_cost,
            "daily_food_cost": daily_food_cost,
            "transport_cost": transport_cost,
            "attraction_cost": attraction_cost,
            "total_budget": total_budget
        }

        self.logger.log_agent_start(self.name, inputs)

        try:
            result = calculate_travel_budget(
                days,
                daily_hotel_cost,
                daily_food_cost,
                transport_cost,
                attraction_cost,
                total_budget
            )

            self.logger.log_tool_call(
                "calculate_travel_budget",
                inputs,
                result
            )

            self.logger.log_agent_end(self.name, "success")

            return {
                "agent": self.name,
                "status": "success",
                "total_expenses": result["total_expenses"],
                "remaining_budget": result["remaining_budget"],
                "within_budget": result["within_budget"],
                "expenses": result["expenses"]
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

    agent = BudgetPlanningAgent()

    result = agent.run(
        days=3,
        daily_hotel_cost=1500,
        daily_food_cost=800,
        transport_cost=2000,
        attraction_cost=1000,
        total_budget=12000
    )

    print("\nBudget Agent Result:")
    print(result)