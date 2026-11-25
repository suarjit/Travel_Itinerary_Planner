🌍 Agentic AI Travel Itinerary Planner

An intelligent, multi-agent travel planning application built using Python, LangGraph, LangChain, and Streamlit.

The Agentic AI Travel Itinerary Planner helps users create personalised, multi-day travel plans based on their destination, trip duration, budget, and transportation preferences.

The project uses specialised agents coordinated through a LangGraph workflow to research destinations, organise attractions, estimate transportation requirements, and calculate travel expenses.

---

📌 1. Project Overview

Planning a trip involves researching destinations, selecting attractions, organising daily activities, estimating transportation, and managing expenses.

This project aims to simplify that process through a modular, multi-agent workflow.

Users provide their travel requirements through an interactive Streamlit dashboard. The system processes those inputs through specialised agents and generates a structured travel itinerary.
## Application Dashboard

![Travel Itinerary Planner Dashboard](screenshots/dashboard.png)

🎯 2. Project Objectives

- Research travel destinations and tourist attractions.
- Generate balanced, day-wise travel itineraries.
- Estimate transportation distances and travel times.
- Calculate accommodation, food, transportation, and attraction expenses.
- Compare estimated expenses against the user's budget.
- Coordinate specialised agents through LangGraph.
- Track workflow states, agent execution, and errors.
- Provide an interactive interface for travel planning.

---

✨ 3. Key Features

Destination Research

- Retrieves destination information and tourist attractions.
- Uses OpenStreetMap services.
- Supports cached destination data as a fallback.

Intelligent Itinerary Planning

- Organises attractions across multiple days.
- Distributes attractions evenly across the trip.
- Generates structured daily activity lists.

Transportation Estimation

- Estimates distances between attractions.
- Calculates approximate travel times.
- Supports different transport modes.

Budget Planning

- Estimates accommodation expenses.
- Calculates food and transportation costs.
- Includes attraction expenses.
- Displays total estimated expenses and remaining budget.
- Indicates whether the trip is within budget.

Multi-Agent Orchestration

- Uses LangGraph to coordinate specialised agents.
- Maintains shared workflow state.
- Implements conditional transitions.
- Handles failures and records errors.

Interactive Dashboard

- Built using Streamlit.
- Accepts user travel preferences.
- Displays trip summaries and day-wise itineraries.
- Shows transportation and budget information.

---

🏗️ 4. System Architecture

The application follows a modular architecture in which specialised agents perform individual tasks.

Agent Components

1. Input Validation

Validates user-provided information, including:

- Destination
- Trip duration
- Budget and cost values
- Transportation mode

Invalid inputs are rejected before the workflow proceeds.

2. Destination Research Agent

Responsible for:

- Retrieving destination information.
- Finding tourist attractions.
- Using OpenStreetMap data sources.
- Supporting cached data when live services fail.

3. Itinerary Planning Agent

Responsible for:

- Receiving destination attractions.
- Distributing attractions across the requested number of days.
- Generating a structured daily itinerary.

4. Transport Agent

Responsible for:

- Processing the generated itinerary.
- Estimating distances between attractions.
- Calculating approximate travel times.
- Preparing daily transportation summaries.

5. Budget Planning Agent

Responsible for:

- Calculating accommodation costs.
- Calculating food expenses.
- Including transportation and attraction costs.
- Determining remaining budget.
- Checking whether the estimated expenses exceed the budget.

Workflow Orchestration

LangGraph manages the execution sequence:

START
  |
  v
Input Validation
  |
  v
Destination Research
  |
  v
Itinerary Planning
  |
  v
Transport Estimation
  |
  v
Budget Planning
  |
  v
END

Each major stage checks its execution status. If a stage fails, the workflow records the error and stops further processing.

---

🛠️ 5. Technologies Used

Technology| Purpose
Python| Core programming language
LangGraph| Workflow orchestration
LangChain| AI application framework
Streamlit| Interactive dashboard
Pandas| Data handling
Requests| API communication
Python-dotenv| Environment configuration
Geopy| Geographic calculations
Pytest| Automated testing

External Data Sources

- OpenStreetMap: Geographic and map-related data.
- Nominatim: Destination geocoding.
- Overpass API: Tourist attraction and location data.

---

📂 6. Project Directory Structure

Travel_Itinerary_Planner/
│
├── src/
│   ├── agents/
│   │   ├── destination_agent.py
│   │   ├── itinerary_agent.py
│   │   ├── transport_agent.py
│   │   └── budget_agent.py
│   │
│   ├── tools/
│   │
│   ├── workflow/
│   │   └── travel_graph.py
│   │
│   └── utils/
│
├── data/
│   └── cache/
│
├── notebooks/
│
├── tests/
│
├── results/
│
├── reports/
│
├── app.py
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md

The directory structure above shows the main project components; additional files may exist in individual folders.

---

⚙️ 7. Installation and Setup

Prerequisites

- Python 3.12 or compatible version
- pip
- Git
- Visual Studio Code (recommended)

Step 1: Clone the Repository

git clone <YOUR_GITHUB_REPOSITORY_URL>

Step 2: Navigate to the Project Directory

cd Travel_Itinerary_Planner

Step 3: Create a Virtual Environment

python -m venv venv

Step 4: Activate the Virtual Environment

For Windows PowerShell:

.\venv\Scripts\Activate.ps1

Step 5: Install Dependencies

pip install -r requirements.txt

---

▶️ 8. Running the Application

Run the Streamlit Dashboard

Execute:

streamlit run app.py

Open the following address in your browser:

http://localhost:8501

Run the Workflow Through the Command Line

python main.py

---

📊 9. Sample Project Output

The application has been successfully tested using Darjeeling, India as a sample destination.

Sample Trip Overview

Metric| Result
Destination| Darjeeling, India
Trip Duration| 3 Days
Total Attractions| 15
Transport Mode| Car
Estimated Distance| 33.6 km
Estimated Travel Time| 57.6 minutes
Total Budget| ₹12,000
Estimated Expenses| ₹9,900
Remaining Budget| ₹2,100

Sample Day-wise Transportation

Day| Distance| Estimated Time
Day 1| 10.47 km| 17.95 min
Day 2| 15.57 km| 26.69 min
Day 3| 7.56 km| 12.96 min

Note: These figures represent one successful sample run. Results may vary depending on the retrieved attraction data and itinerary ordering.

---

🧪 10. Testing and Evaluation

The project includes automated tests using Pytest.

Run the test suite:

pytest -v

The test suite previously completed with:

29 passed

Testing covers important project components, including input validation and workflow functionality.

The application has also been manually tested through its Streamlit dashboard.

---

⚠️ 11. Limitations

- Transportation estimates are based on approximate straight-line distances rather than verified road routes.
- Travel times are estimates and do not account for real-time traffic.
- Live OpenStreetMap services may occasionally experience delays or failures.
- Cached destination information is currently limited to selected destinations, including Darjeeling.
- Budget calculations are estimates and may differ from actual travel expenses.
- The current agents primarily use Python-based logic and tools coordinated through LangGraph; the project is not yet a fully autonomous LLM-agent system.

---

🚀 12. Future Enhancements

Potential improvements include:

- Integrating road-routing APIs for more accurate transportation estimates.
- Adding weather information and forecasts.
- Expanding destination coverage.
- Improving personalised attraction recommendations.
- Adding map-based itinerary visualisation.
- Integrating accommodation and transportation information.
- Improving agent reasoning and decision-making.
- Adding more comprehensive evaluation scenarios.

---

💡 13. Challenges and Solutions

Challenge| Approach
Live API failures| Implemented cached destination data
Uneven attraction distribution| Used balanced itinerary distribution
Workflow failures| Added conditional transitions and error handling
Transportation estimation| Implemented geographic distance estimation
Budget management| Created a separate budget planning agent
Workflow monitoring| Added logging and state transition tracking

---

📌 14. Project Status

Core workflow implemented and Streamlit dashboard successfully tested.

The project includes:

- Five main workflow stages.
- Specialised Python-based agents.
- LangGraph orchestration.
- Destination data retrieval and caching.
- Multi-day itinerary generation.
- Transportation estimation.
- Budget calculation.
- Interactive Streamlit dashboard.
- Automated tests.

Documentation, final validation, and repository publication are the remaining project tasks.

---

👨‍💻 15. Author

Project: Agentic AI Travel Itinerary Planner

Domain: Agentic AI / Python / Data Science

Framework: LangGraph and Streamlit

---

Built as a project exploring multi-agent workflow orchestration and intelligent travel planning.