import streamlit as st

# Session state to store player names
if 'players' not in st.session_state:
    st.session_state.players = []

# Function to add a player
def add_player(name):
    st.session_state.players.append(name)

# Page title
st.title("Game Day Player Registration")

# Add player form
with st.form(key='player_form'):
    player_name = st.text_input("Enter your name:")
    submit_button = st.form_submit_button("Add Player")

    if submit_button and player_name:
        add_player(player_name)
        st.success(f"Player {player_name} added to the list!")

# Display list of players
st.subheader("Players for Today:")
if st.session_state.players:
    st.write(", ".join(st.session_state.players))
else:
    st.write("No players have been added yet.")
