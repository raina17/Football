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
    c.execute('SELECT name FROM players')
    players = [row[0] for row in c.fetchall()]
    conn.close()
    return players

def reset_players_in_db():
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

    /* Make the "Add Player" button red with black text */
    .stButton:first-of-type > button {{
        background-color: red !important;
        color: black !important;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        
    }}

    /* Make the "Reset List" button red with black text */
    .stButton:nth-of-type(2) > button {{
        background-color: red !important;
        color: black !important;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# Set background image
set_background("rldo.jpg")  # Replace with your image file name

# --- Game Day Player Registration Title ---
st.markdown("<h1 style='color:white;'>Sunday, 19th Jan</h1>", unsafe_allow_html=True)

# --- Player Registration Form ---
with st.form(key='player_form'):
    player_name = st.text_input("Enter your name:", max_chars=30)
    submit_button = st.form_submit_button("Add Player")

    if submit_button and player_name.strip():
        add_player_to_db(player_name.strip())
        st.success(f"Player {player_name} added to the list!")

st.markdown("<h2>Players for the game:</h2>", unsafe_allow_html=True)
players = get_players_from_db()
if players:
    for index, player in enumerate(players, start=1):
        st.markdown(f"<p style='color:white;'> {index}. {player}</p>", unsafe_allow_html=True)
else:
    st.write("No players have been added yet.")

st.markdown("<h3>Venue for the Game:</h2>", unsafe_allow_html=True)
st.write("To be decided")


# --- Admin Controls ---
st.subheader("Admin Controls")
admin_password = st.text_input("Enter admin password to reset the list:", type="password")
reset_button = st.button("Reset List")
if reset_button:
    if admin_password == "admin123":  # Change this password to something secure
        reset_players_in_db()
        st.success("Player list has been reset!")
    else:
        st.error("Incorrect admin password.")
