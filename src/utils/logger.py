
import json
import os
from datetime import datetime

class WorkflowLogger:
    """
    Records agent execution, tool calls, inputs, outputs and errors.
    """

    def __init__(self, log_file="results/workflow_trace.jsonl"):
        self.log_file = log_file

        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

    def log_event(self, event_type, details):

        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "details": details
        }

        with open(self.log_file, "a", encoding="utf-8") as file:
            file.write(json.dumps(event, ensure_ascii=False, default=str) + "\n")

        print(f"[TRACE] {event_type}: {details}")

    def log_agent_start(self, agent_name, inputs):
        self.log_event("agent_started", {
            "agent": agent_name,
            "inputs": inputs
        })

    def log_tool_call(self, tool_name, inputs, output):
        self.log_event("tool_call", {
            "tool": tool_name,
            "inputs": inputs,
            "output": output
        })

    def log_agent_end(self, agent_name, status):
        self.log_event("agent_completed", {
            "agent": agent_name,
            "status": status
        })

    def log_error(self, component, error):
        self.log_event("error", {
            "component": component,
            "error": str(error)
        })