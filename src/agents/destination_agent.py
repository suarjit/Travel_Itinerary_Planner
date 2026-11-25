
from src.tools.destination_tool import research_destination
from src.utils.logger import WorkflowLogger

class DestinationResearchAgent:

    def __init__(self):
        self.name = "Destination Research Agent"
        self.logger = WorkflowLogger()

    def run(self, destination):

        print(f"{self.name} started...")
        print(f"Researching destination: {destination}")

        self.logger.log_agent_start(
            self.name,
            {"destination": destination}
        )

        try:
            result = research_destination(destination)

            self.logger.log_tool_call(
                "research_destination",
                {"destination": destination},
                result
            )

            if not result.get("success", False):
                self.logger.log_agent_end(self.name, "failed")

                return {
                    "agent": self.name,
                    "status": "failed",
                    "message": result.get("message", "Research failed")
                }

            self.logger.log_agent_end(self.name, "success")

        

            return {
                "agent": self.name,
                "status": "success",
                "destination": result["destination"],
                "attractions": result["attractions"],
                "total_attractions": result["total_attractions"],
                "data_source": result.get("data_source", "Unknown"),
                "cached": result.get("cached", False)
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

    agent = DestinationResearchAgent()
    result = agent.run("Darjeeling, India")

    print("\nAgent Result:")
    print(result)