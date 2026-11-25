
import streamlit as st

from src.workflow.travel_graph import run_travel_workflow

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Travel Itinerary Planner",
    page_icon="✈️",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM STYLING
# --------------------------------------------------

st.markdown("""
<style>
.main-title {
    font-size: 38px;
    font-weight: 700;
    text-align: center;
    color: #2563EB;
}

.subtitle {
    text-align: center;
    font-size: 17px;
    color: gray;
}

.section-title {
    font-size: 25px;
    font-weight: 600;
    margin-top: 25px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# APPLICATION HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">✈️ AI Travel Itinerary Planner</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your intelligent travel planning assistant</div>',
    unsafe_allow_html=True
)

st.divider()

# --------------------------------------------------
# TRAVEL INPUT FORM
# --------------------------------------------------

st.header("🌍 Plan Your Trip")

with st.form("travel_form"):

    destination = st.text_input(
        "Destination",
        placeholder="Example: Darjeeling, India"
    )

    col1, col2 = st.columns(2)

    with col1:

        days = st.number_input(
            "Number of Days",
            min_value=1,
            max_value=30,
            value=3,
            step=1
        )

    with col2:

        transport_mode = st.selectbox(
            "Transport Mode",
            ["car", "bus", "train", "walking"]
        )

    st.subheader("💰 Budget Details")

    col1, col2 = st.columns(2)

    with col1:

        daily_hotel_cost = st.number_input(
            "Daily Hotel Cost (₹)",
            min_value=0,
            value=1500
        )

        daily_food_cost = st.number_input(
            "Daily Food Cost (₹)",
            min_value=0,
            value=800
        )

        transport_cost = st.number_input(
            "Total Transport Cost (₹)",
            min_value=0,
            value=2000
        )

    with col2:

        attraction_cost = st.number_input(
            "Total Attraction Cost (₹)",
            min_value=0,
            value=1000
        )

        total_budget = st.number_input(
            "Your Total Budget (₹)",
            min_value=0,
            value=12000
        )

    submit = st.form_submit_button(
        "🚀 Generate Travel Plan",
        use_container_width=True
    )

# --------------------------------------------------
# GENERATE TRAVEL PLAN
# --------------------------------------------------

if submit:

    if not destination.strip():

        st.warning("Please enter a destination.")

    elif total_budget <= 0:

        st.warning("Please enter a budget greater than zero.")

    else:

        try:

            with st.spinner("🤖 AI agents are planning your trip..."):

                result = run_travel_workflow(
                    destination=destination,
                    days=int(days),
                    daily_hotel_cost=daily_hotel_cost,
                    daily_food_cost=daily_food_cost,
                    transport_cost=transport_cost,
                    attraction_cost=attraction_cost,
                    total_budget=total_budget,
                    transport_mode=transport_mode
                )

            if result.get("status") != "success":

                st.error("Unable to generate the travel plan.")

                st.write("Errors:", result.get("errors", []))

            else:

                st.success("Your travel plan is ready!")

                # ----------------------------------
                # GET WORKFLOW RESULTS
                # ----------------------------------

                itinerary_info = result.get(
                    "itinerary_info", {}
                )

                transport_info = result.get(
                    "transport_info", {}
                )

                budget_info = result.get(
                    "budget_info", {}
                )

                daily_itinerary = itinerary_info.get(
                    "daily_itinerary", []
                )

                daily_transport = transport_info.get(
                    "daily_transport", []
                )
        

                expenses = budget_info.get(
                    "expenses", {}
                )

                total_attractions = itinerary_info.get(
                    "total_attractions", 0
                )

                total_distance = transport_info.get(
                    "total_distance_km", 0
                )

                total_travel_time = transport_info.get(
                    "total_travel_time_minutes", 0
                )

                total_expenses = budget_info.get(
                    "total_expenses", 0
                )

                remaining_budget = budget_info.get(
                    "remaining_budget", 0
                )

                # ----------------------------------
                # TRIP OVERVIEW
                # ----------------------------------

                st.divider()

                st.header("📊 Trip Overview")

                col1, col2, col3, col4 = st.columns(4)

                col1.metric(
                    "Trip Duration",
                    f"{days} Days"
                )

                col2.metric(
                    "Attractions",
                    total_attractions
                )

                col3.metric(
                    "Total Distance",
                    f"{total_distance} km"
                )

                col4.metric(
                    "Remaining Budget",
                    f"₹{remaining_budget:,.0f}"
                )

                # ----------------------------------
                # DAY-WISE ITINERARY
                # ----------------------------------

                st.divider()

                st.header("📍 Your Day-wise Itinerary")

                for day_plan in daily_itinerary:

                    day_number = day_plan.get("day", 0)

                    activities = day_plan.get(
                        "activities", []
                    )

                    with st.expander(
                        f"Day {day_number} — {len(activities)} Attractions",
                        expanded=True
                    ):

                        for index, activity in enumerate(
                            activities, start=1
                        ):

                            if isinstance(activity, dict):

                                attraction_name = activity.get(
                                    "name", "Unknown attraction"
                                )

                            else:

                                attraction_name = str(activity)

                            st.write(
                                f"**{index}.** 📍 {attraction_name}"
                            )

                # ----------------------------------
                # TRANSPORT INFORMATION
                # ----------------------------------

                st.divider()

                st.header("🚗 Transport Information")

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Total Distance",
                    f"{total_distance} km"
                )

                col2.metric(
                    "Estimated Travel Time",
                    f"{total_travel_time} min"
                )

                col3.metric(
                    "Transport Mode",
                    transport_mode.title()
                )

                st.subheader("Daily Transport Details")

                for day_transport in daily_transport:

                    day_number = day_transport.get(
                        "day", 0
                    )

                    with st.expander(
                        f"Day {day_number} Transport",
                           expanded=True
                        ):

                        st.write(
                            "Distance:",
                            f"{day_transport.get('total_distance_km', 0)} km"
                        )

                        st.write(
                            "Travel Time:",
                            f"{day_transport.get('total_travel_time_minutes', 0)} minutes"
                        )

                        st.write("Journey Details:")

                        for journey in day_transport.get(
                            "journeys", []
                        ):

                            st.write(
                                f"📍 {journey.get('destination', 'Unknown')} — "
                                f"{journey.get('distance_km', 0)} km, "
                                f"{journey.get('estimated_travel_time_minutes', 0)} minutes"
                            )

                st.caption(
                    transport_info.get(
                        "note",
                        "Transport values are approximate estimates."
                    )
                )

                # ----------------------------------
                # BUDGET INFORMATION
                # ----------------------------------

                st.divider()

                st.header("💰 Budget Overview")

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Total Budget",
                    f"₹{total_budget:,.0f}"
                )

                col2.metric(
                    "Total Expenses",
                    f"₹{total_expenses:,.0f}"
                )

                col3.metric(
                    "Remaining Budget",
                    f"₹{remaining_budget:,.0f}"
                )

                if budget_info.get("within_budget", False):

                    st.success(
                        "Your trip is within the planned budget!"
                    )

                else:

                    st.warning(
                        "Your trip exceeds the planned budget."
                    )

                st.subheader("Expense Breakdown")

                expense_labels = {
                    "accommodation": "Accommodation",
                    "food": "Food",
                    "transport": "Transport",
                    "attractions": "Attractions"
                }

                for expense_key, expense_label in expense_labels.items():

                    amount = expenses.get(expense_key, 0)

                    st.write(
                        f"**{expense_label}:** ₹{amount:,.0f}"
                    )

                if total_expenses > 0:

                    st.progress(
                        min(total_expenses / total_budget, 1.0)
                    )

                st.caption(
                    "Budget estimates are based on the costs entered in the form."
                )

                st.divider()

                st.success(
                    "Thank you for using AI Travel Itinerary Planner!"
                )

        except Exception as error:

            st.error("An unexpected error occurred.")

            st.exception(error)