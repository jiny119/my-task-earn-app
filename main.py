import streamlit as st
import json
import os
import webbrowser

# ---------------------------
# JSON Database Functions
# ---------------------------
DB_FILE = "users.json"

def load_users():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

# ---------------------------
# Global Data
# ---------------------------
users_db = load_users()  # {username: { "password": ..., "coins": ..., "referrals": ..., "clicks": ... }}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "theme" not in st.session_state:
    st.session_state.theme = "Light"

# ---------------------------
# Helper Functions
# ---------------------------
def create_user(username, password):
    """Create a new user in the JSON database."""
    users_db[username] = {
        "password": password,
        "coins": 0,
        "referrals": 0,
        "clicks": 0
    }
    save_users(users_db)

def user_exists(username):
    return username in users_db

def check_password(username, password):
    return users_db[username]["password"] == password

def get_coins(username):
    return users_db[username]["coins"]

def add_coins(username, amount):
    users_db[username]["coins"] += amount
    save_users(users_db)

def get_referrals(username):
    return users_db[username]["referrals"]

def add_referral(username):
    users_db[username]["referrals"] += 1
    save_users(users_db)

def get_clicks(username):
    return users_db[username]["clicks"]

def add_click(username):
    users_db[username]["clicks"] += 1
    save_users(users_db)

# ---------------------------
# Pages
# ---------------------------

# Sign Up Page
def signup_page():
    st.title("Create a New Account")
    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        if user_exists(new_user):
            st.warning("⚠️ Username already exists! Try another.")
        else:
            create_user(new_user, new_pass)
            st.success("✅ Account created successfully! Please log in now.")

# Login Page
def login_page():
    st.title("Log In")
    user = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Log In"):
        if user_exists(user) and check_password(user, password):
            st.session_state.logged_in = True
            st.session_state.username = user
            st.success(f"✅ Welcome, {user}!")
        else:
            st.error("❌ Invalid username or password.")

# Settings Page
def settings_page():
    st.title("Settings")

    # Theme Change
    theme_choice = st.selectbox("Select Theme", ["Light", "Dark", "Blue"])
    st.session_state.theme = theme_choice
    st.success(f"Theme changed to {theme_choice}!")

    # Withdrawal System
    st.subheader("💸 Withdraw Earnings")

    username = st.session_state.username
    coins = get_coins(username)
    refs = get_referrals(username)
    clicks = get_clicks(username)

    st.write(f"**Your Balance:** {coins} coins")
    st.write(f"**Referrals:** {refs}/10")
    st.write(f"**Clicks:** {clicks}/5")
    st.write("**Minimum:** 15000 coins + 10 referrals + 5 clicks required for withdrawal.")

    if coins >= 15000 and refs >= 10 and clicks >= 5:
        withdraw_amount = st.number_input("Enter amount to withdraw", min_value=15000, max_value=coins, step=500)
        method = st.selectbox("Select Payment Method", ["JazzCash", "EasyPaisa", "Payoneer", "PayPal"])
        if st.button("Request Withdrawal"):
            st.success(f"✅ Withdrawal request of {withdraw_amount} coins via {method} submitted!")
    else:
        st.warning("⚠️ You do not meet the withdrawal requirements yet.")

    # Logout Button
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.success("✅ Logged out successfully!")

# Task Page
def task_page():
    st.title("🎯 Earn & Win App")

    # Settings Icon (Top Right Corner)
    st.markdown(
        """
        <div style="position: fixed; top: 10px; right: 10px;">
            <a href="?page=settings">
                <img src="https://cdn-icons-png.flaticon.com/512/2099/2099058.png" width="40" />
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write(f"Welcome, {st.session_state.username}! Complete tasks below to earn coins:")

    username = st.session_state.username

    # Survey Task (YouTube Channel + Video)
    st.subheader("1) Complete Survey & Earn (YouTube)")
    if st.button("Complete Survey"):
        # Open Channel
        webbrowser.open_new_tab("https://www.youtube.com/@ToonCraftStudio-f7o?sub_confirmation=1")
        st.info("Please Subscribe, then click 'Watch Video' below.")
    if st.button("Watch Video"):
        webbrowser.open_new_tab("https://youtu.be/trr3AC1jiEk?si=CKMZeDaMnLhFRUJ6")
        add_coins(username, 20)
        st.success("✅ You earned 20 coins for completing the survey!")

    # Play Game & Earn
    st.subheader("2) Play Game & Earn")
    if st.button("Play Game"):
        webbrowser.open_new_tab("https://poki.com/en/g/gumball-darwin-s-yearbook")
        add_coins(username, 5)
        st.success("✅ You earned 5 coins!")

    # Install App & Earn
    st.subheader("3) Install App & Earn")
    if st.button("Install App"):
        webbrowser.open_new_tab("https://play.google.com/store/apps/details?id=com.spotify.music")
        add_coins(username, 5)
        st.success("✅ You earned 5 coins!")

    # Watch Ads & Earn
    st.subheader("4) Watch Ads & Earn")
    if st.button("Watch Ads"):
        st.warning("⚠️ AdSense Approval needed. Pretend you watched an ad.")
        add_coins(username, 5)
        st.success("✅ You earned 5 coins!")

    # Referral
    st.subheader("5) Refer a Friend & Earn")
    if st.button("Refer a Friend"):
        add_referral(username)
        add_coins(username, 5)
        st.success("✅ You earned 5 coins for referral!")

    # Click Ads
    st.subheader("6) Click Ads & Earn")
    if st.button("Click Ads"):
        add_click(username)
        add_coins(username, 5)
        st.success("✅ You earned 5 coins for clicking ads!")

# Navigation Logic
def main():
    # بدل دیا گیا: st.experimental_get_query_params -> st.query_params
    query_params = st.query_params
    page = query_params.get("page", [""])[0]

    if not st.session_state.logged_in:
        # Show Sign Up / Login options
        choice = st.sidebar.radio("Menu", ["Log In", "Sign Up"])
        if choice == "Log In":
            login_page()
        else:
            signup_page()
    else:
        if page == "settings":
            settings_page()
        else:
            task_page()

if __name__ == "__main__":
    main()
