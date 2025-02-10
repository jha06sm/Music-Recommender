import streamlit as st
from googleapiclient.discovery import build

# YouTube API Key (replace with your own)
API_KEY = "AIzaSyDv3WrvzLZDcmuKxAbIhzxBeeYn6fOr6VY"

# Initialize YouTube API client
youtube = build("youtube", "v3", developerKey=API_KEY)

# Define a dictionary for emotion-to-query mapping
emotion_to_query = {
    "happy": "happy pop music",
    "sad": "sad acoustic songs",
    "calm": "calm piano music",
    "energetic": "high energy workout music",
    "romantic": "romantic love songs",
    "angry": "heavy metal music",
    "nostalgic": "90s throwback songs",
    "motivated": "workout motivation music",
    "chill": "lo-fi chill beats",
    "focused": "study focus music",
    # Add more emotions and corresponding search queries
}

# Function to search for songs on YouTube
def search_youtube(query, max_results=5):
    request = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        maxResults=max_results
    )
    response = request.execute()
    recommendations = []
    if response["items"]:
        for item in response["items"]:
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            recommendations.append({"title": title, "video_id": video_id})
    return recommendations

# Streamlit App
st.title("GSJ-Grand Sonic Journey")



st.write("welcome to the jha's verse")

# Dropdown for mood selection
moods = list(emotion_to_query.keys())  # Get all moods from the dictionary
selected_mood = st.selectbox("How are you feeling today?", moods)

# Number of recommendations
num_recommendations = st.slider("Number of recommendations", 1, 10, 5)

# Recommend and display music
if st.button("Recommend Music"):
    st.write(f"🎧 Searching for music for '{selected_mood}'...")
    
    # Get music recommendations from the dictionary
    query = emotion_to_query[selected_mood]
    recommendations = search_youtube(query, max_results=num_recommendations)
    
    if recommendations:
        st.write(f"Here are {len(recommendations)} songs for you:")
        for idx, rec in enumerate(recommendations, start=1):
            st.write(f"### {idx}. {rec['title']}")
            st.write(f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{rec["video_id"]}" frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)
    else:
        st.warning("No results found for your mood.")