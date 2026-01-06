import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(page_title="UMPSA For You", layout="wide")
st.title("🎯UMPSA FOR YOU PAGE")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_excel(r"D:\SEM 5\BSD3513 INTRO AI\GPE_AI\tiktok.xlsx")
    
    # Convert Duration to seconds
    def get_seconds(time_str):
        try:
            total_sec = 0
            if 'm' in time_str:
                parts = time_str.split('m')
                total_sec += int(parts[0].strip()) * 60
                time_str = parts[1]
            if 's' in time_str:
                total_sec += int(time_str.replace('s', '').strip())
            return total_sec
        except:
            return 0
            
    df['duration_seconds'] = df['Duration'].apply(get_seconds)
    return df

try:
    content = load_data()
except Exception as e:
    st.error(f"Error loading file: {e}")
    st.stop()

# -------------------
# Sidebar: user input
# -------------------
st.sidebar.header("Your Profile")

faculty = st.sidebar.selectbox(
    "Select Faculty", 
    ["FTKKP", "FTKA", "FTKEE", "FTKPM", "FTKMA", "FK", "FIST", "FIM", "PSM", "All"]
)

# Using your specific list for 'Select Your Interest'
category = st.sidebar.selectbox(
    "Select Your Interest", 
    ["All","daily", "physics", "biotechnology", "electronics", "enviromental", "materials science", "nanotechnology", "energy",
     "computer science", "cybersecurity", "data science", "statistic", "3d printing", "robotics", "mechanical engineering", "civil engineering",
     "biomedical engineering", "chemical engineering", "architecture", "math", "game theory", "coding", "psychology", "art", "life hack", "invention", "ethic"]
)

# -------------------
# Main Content UI
# -------------------
search_query = st.text_input("🔍 Search Videos", placeholder="Search here...")

# -------------------
# Filter and Sort Logic
# -------------------

# 1. Faculty 
if faculty != "All":
    filtered = content[(content["Faculty"] == faculty) | (content["Faculty"] == "ALL")]
else:
    filtered = content.copy()

# 2. Category 
if category != "All":
    filtered = filtered[filtered["Category"] == category]

# 3. Search Bar
if search_query:
    filtered = filtered[filtered["title"].str.contains(search_query, case=False, na=False)]

# 4. Sorting Comment and Duration
recommended = filtered.sort_values(
    by=["Comment_Count", "duration_seconds"], 
    ascending=[False, False]
)

# -------------------
# Display Feed
# -------------------
st.subheader(f"Recommended {category.title()} Content")
st.write(f"Showing {len(recommended)} results")

if recommended.empty:
    st.warning("No matches found for your current selection.")
else:
    rows = [recommended.iloc[i:i+3] for i in range(0, len(recommended), 3)]
    
    for row_data in rows:
        cols = st.columns(3)
        for i, (_, row) in enumerate(row_data.iterrows()):
            with cols[i]:
                with st.container(border=True):
                    st.markdown(f"### {row['title']}")
                    st.write(f"**Type:** {row['Type']}")
                    st.write(f"**Faculty:** {row['Faculty']}")
                    
                    col_stats1, col_stats2 = st.columns(2)
                    col_stats1.write(f"💬 {row['Comment_Count']} Comments")
                    col_stats2.write(f"⏳ {row['Duration']}")
                    
                    st.caption(f"Posted on: {row['Date_Posted']}")
                    
                    
