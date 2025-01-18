import streamlit as st
import sqlite3
import base64

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect('players.db')
    c = conn.cursor()
    c.execute(''' 
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_player_to_db(name):
    conn = sqlite3.connect('players.db')
    c = conn.cursor()
    c.execute('INSERT INTO players (name) VALUES (?)', (name,))
    conn.commit()
    conn.close()

def get_players_from_db():
    conn = sqlite3.connect('players.db')
    c = conn.cursor()
    c.execute('SELECT id, name FROM players')
    players = c.fetchall()
    conn.close()
    return players

def delete_player_from_db(player_id):
    conn = sqlite3.connect('players.db')
    c = conn.cursor()
    c.execute('DELETE FROM players WHERE id = ?', (player_id,))
    conn.commit()
    conn.close()

def delete_all_players():
    conn = sqlite3.connect('players.db')
    c = conn.cursor()
    c.execute('DELETE FROM players')
    conn.commit()
    conn.close()

# Initialize database
init_db()

# --- Streamlit UI ---
# Helper function to set background
def set_background(image_path):
    with open(image_path, "rb") as file:
        encoded_string = base64.b64encode(file.read()).decode()
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{encoded_string}");
        background-size: contain;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        height: 100vh;
        width: 100%;
    }}

    /* Styling text to be left-aligned and white */
    h1, h2, p {{
        color: white;
        text-align: left;
        margin-top: 20px;
        margin-left: 20px; /* Align to the left */
    }}

    /* Customizing the text input */
    .css-1kyxreq {{
        color: white;
        text-align: left;
    }}

    .css-2trqjy {{
        color: white;
        text-align: left;
    }}

    /* Styling the Login button */
    div.stButton > button:first-child {{
        background-color: red;
        color: white;
        border: none;
        padding: 0.5em 1em;
        border-radius: 5px;
        font-size: 16px;
        cursor: pointer;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


# Set background image
set_background("giphy.gif")  # Replace with your image file name

# --- Login Page ---
def login_page():
    st.title("User Login")
    name = st.text_input("Enter your name:")
    if st.button("Login"):
        if name.strip():
            st.session_state['user_name'] = name.strip()
            main_page()
        else:
            st.error("Please enter your name to continue.")

# --- Main Page ---
def main_page():
    st.markdown("<h1 style='color:white; font-size: 24px;'>Sunday, 19th Jan 7:30-9 AM</h1>", unsafe_allow_html=True)

    # --- Player Registration ---
    if st.button("Add Your Name"):
        user_name = st.session_state.get('user_name', '').strip()
        if user_name:
            add_player_to_db(user_name)
            st.success(f"Player {user_name} added to the list!")
        else:
            st.error("No name found. Please login again.")

    st.markdown("<h2 style='color:white; font-size: 24px;'>Players for the game:</h2>", unsafe_allow_html=True)
    players = get_players_from_db()
    current_user = st.session_state.get('user_name', '').strip()
    if players:
        for index, (player_id, player_name) in enumerate(players, start=1):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"<p style='color:white;'> {index}. {player_name}</p>", unsafe_allow_html=True)
            if player_name == current_user:
                with col2:
                    if st.button("Remove", key=f"remove_{player_id}"):
                        delete_player_from_db(player_id)
                        st.rerun()
    else:
        st.write("No players have been added yet.")

    st.markdown("<h3 style='color:white; font-size: 24px;'>Venue for the Game:</h3>", unsafe_allow_html=True)
    st.write("To be decided")

    # --- Admin Reset Section ---
    admin_password = st.text_input("Enter Admin Password to Reset Players List", type="password")
    if admin_password == "admin123":  # Replace with your desired admin password
        if st.button("Reset Players List"):
            delete_all_players()
            st.success("Players list has been reset!")
    elif admin_password:
        st.error("Incorrect admin password.")

# --- Main App Logic ---
if 'user_name' not in st.session_state:
    login_page()
else:
    main_page()
