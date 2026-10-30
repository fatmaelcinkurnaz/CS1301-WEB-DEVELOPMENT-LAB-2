# This creates the page for displaying data visualizations.

import streamlit as st
import json
import plotly.express as px

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")


# PART 1: GRAPHS FROM data.json
# --- YOUR CODE GOES HERE ---



# PART 1: GRAPHS FROM data.json

# Load data from JSON
with open("data.json", "r") as infile:
    data = json.load(infile)

players = data[0]["Player"]
ratings = data[0]["Rating"]
birth_years = data[0]["Birth Year"]

# GRAPH 1: Rating differences
st.subheader("How Close Are the Players' Ratings?")

lowest_rating = min(ratings)

player_data = sorted(
    zip(players, ratings),
    key=lambda item: item[1],
    reverse=True
)

sorted_players = [item[0] for item in player_data]
sorted_ratings = [item[1] for item in player_data]
rating_gaps = [rating - lowest_rating for rating in sorted_ratings]

fig1 = px.bar(
    x=rating_gaps,
    y=sorted_players,
    orientation="h",
    text=rating_gaps,
    title="Rating Advantage Compared with the Lowest-Rated Player",
    labels={
        "x": "Rating Points Above the Lowest Rating",
        "y": "Chess Player"
    }
)

fig1.update_traces(textposition="outside")
fig1.update_layout(
    yaxis={"autorange": "reversed"},
    xaxis={"rangemode": "tozero"},
    showlegend=False
)

st.plotly_chart(fig1, use_container_width=True)

st.caption(
    "Each bar shows how many rating points a player has "
    "above the lowest rating in this dataset."
)

# GRAPH 2: Interactive birth year vs. rating
st.subheader("Does Birth Year Relate to Chess Rating?")

if "minimum_rating" not in st.session_state:
    st.session_state["minimum_rating"] = min(ratings)

minimum_rating = st.slider(
    "Show players with at least this rating:",
    min_value=min(ratings),
    max_value=max(ratings),
    value=st.session_state["minimum_rating"],
    step=5,
    key="minimum_rating"
)

filtered_data = [
    (player, rating, year)
    for player, rating, year in zip(players, ratings, birth_years)
    if rating >= minimum_rating
]

if filtered_data:
    filtered_players = [item[0] for item in filtered_data]
    filtered_ratings = [item[1] for item in filtered_data]
    filtered_birth_years = [item[2] for item in filtered_data]

    fig2 = px.scatter(
        x=filtered_birth_years,
        y=filtered_ratings,
        text=filtered_players,
        title="Player Birth Year vs. FIDE Rating",
        labels={
            "x": "Birth Year",
            "y": "FIDE Rating"
        },
        hover_name=filtered_players
    )

    fig2.update_traces(textposition="top center")
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("No players match the selected rating threshold.")



# PART 2: GRAPHS FROM data.csv
# --- YOUR CODE GOES HERE ---
