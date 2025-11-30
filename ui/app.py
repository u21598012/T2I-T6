import streamlit as st
import requests
import json

# --------------------------------------------
# PAGE CONFIG
# --------------------------------------------
st.set_page_config(
    page_title="Health Advice Chatbot",
    page_icon="🏥",
    layout="wide"
)

API_URL = "http://localhost:5001"

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user" not in st.session_state:
    st.session_state.user = ""
if "messages" not in st.session_state:
    st.session_state.messages = []
if "patient_info" not in st.session_state:
    st.session_state.patient_info = {}
if "diet_info" not in st.session_state:
    st.session_state.diet_info = {"meals": {}}

# Simple user database
USER_DB = {
    "Tech2Impact": "password123",
    "admin": "admin123"
}


# ============================================================
# LOGIN PAGE
# ============================================================
def login_page():
    col1, col2, col3 = st.columns([1, 20, 1 ])

    with col2:
        st.image("logo.png", width=150)
        st.title("Health Advice System")
        st.markdown("🔐 Login")
        st.markdown("---")

        with st.form("login_form"):
            fullname = st.text_input("Full Name", placeholder="Enter your Full Name")
            password = st.text_input("Password", type="password", placeholder="Enter your password")

            submit = st.form_submit_button("Login", use_container_width=True)

            if submit:
                if fullname in USER_DB and USER_DB[fullname] == password:
                    st.session_state.authenticated = True
                    st.session_state.user = fullname
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Please try again.")

        st.markdown("---")


# ============================================================
# MAIN APPLICATION
# ============================================================
def main_application():

    # --------------------------------------------
    # SIDEBAR MENU
    # --------------------------------------------
    with st.sidebar:
        st.markdown(f"### 👤 Welcome: **{st.session_state.user}**")
        st.markdown("---")

        page_selection = st.radio(
        "Navigation",
        ["Chat", "Patient Info"]
)

        st.markdown("---")



        st.markdown("---")

        if st.button("🧹 Clear Chat History"):
            st.session_state.messages = []
            st.rerun()

        #st.markdown("---")

        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.user = ""
            st.session_state.messages = []
            st.rerun()

    # ============================================================
    # PAGE: CHAT
    # ============================================================
    if page_selection == "Chat":
        st.image("logo.png", width=150)
        st.title("💬 Health Advice Chatbot")

        # Show chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input
        if prompt := st.chat_input("Ask for health advice..."):

            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                msg_box = st.empty()

                try:
                    response = requests.post(
                        f"{API_URL}/health-advice",
                        json={
                            "prompt": prompt,
                            "patient": st.session_state.patient_info,
                            "diet": st.session_state.diet_info,
                        },
                        timeout=60
                    )

                    if response.status_code == 200:
                        bot_reply = response.json().get("response", "No response.")
                    else:
                        bot_reply = "⚠️ API error."

                except Exception:
                    bot_reply = "⚠️ Could not connect to API."

                msg_box.markdown(bot_reply)

            st.session_state.messages.append(
                {"role": "assistant", "content": bot_reply}
            )

    # ============================================================
    # PAGE: PATIENT INFO
    # ============================================================
    elif page_selection == "Patient Info":
        st.image("logo.png", width=150)
        st.title("🧑‍⚕️ Patient Information")

        st.markdown("Fill or edit your details:")

        pi = st.session_state.patient_info

        # -----------------------
        # Patient Basic Info Form
        # -----------------------
        with st.form("patient_form"):
            col1, col2 = st.columns(2)

            with col1:
                name = st.text_input("Name", pi.get("name", ""))
                age = st.number_input("Age", min_value=0, max_value=120, step=1, value=pi.get("age", 0))

            with col2:
                surname = st.text_input("Surname", pi.get("surname", ""))
                gender = st.selectbox(
                    "Gender",
                    ["Male", "Female", "Other"],
                    index=["Male", "Female", "Other"].index(pi.get("gender", "Male"))
                )

            st.write("---")

            chronic_disease = st.selectbox(
                "Chronic Disease",
                ["Diabetes", "Hypertension"],
                index=["Diabetes", "Hypertension"].index(pi.get("chronic_disease", "Diabetes"))
            )

            current_status = st.text_area("Current Status", pi.get("current_status", ""))

            allergies = st.text_input("Allergies", pi.get("allergies", ""))

            save_patient = st.form_submit_button("💾 Save Patient Info")

            if save_patient:
                st.session_state.patient_info = {
                    "name": name,
                    "surname": surname,
                    "age": age,
                    "gender": gender,
                    "chronic_disease": chronic_disease,
                    "current_status": current_status,
                    "allergies": allergies
                }
                st.success("Patient information updated!")

        st.write("---")

        # -----------------------
        # Meals Form
        # -----------------------
        st.subheader("🍽️ Daily Meals")

        with st.form("meals_form"):
            meals = st.session_state.diet_info.get("meals", {})

            breakfast = st.text_area("Breakfast", meals.get("breakfast", ""))
            lunch = st.text_area("Lunch", meals.get("lunch", ""))
            dinner = st.text_area("Dinner / Supper", meals.get("dinner", ""))

            save_meals = st.form_submit_button("💾 Save Meal Info")

            if save_meals:
                st.session_state.diet_info["meals"] = {
                    "breakfast": breakfast,
                    "lunch": lunch,
                    "dinner": dinner
                }
                st.success("Meal information updated!")

        # Show saved info
        #st.subheader("📄 Current Saved Information")
        #st.json(st.session_state.patient_info)
        #st.json(st.session_state.diet_info)


# ============================================================
# ROUTING
# ============================================================
if st.session_state.authenticated:
    main_application()
else:
    login_page()
