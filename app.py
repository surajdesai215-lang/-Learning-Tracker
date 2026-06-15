import streamlit as st
from datetime import date

st.set_page_config(
    page_title="Data Science Learning Tracker",
    page_icon="📚",
    layout="wide"
)

st.title("📚  Learning Tracker")

# Session State
if "topics" not in st.session_state:
    st.session_state.topics = []

# -----------------------------
# Add New Topic
# -----------------------------
st.header("➕ Add New Topic")

topic_name = st.text_input("📖 Topic Name")

notes = st.text_area(
    "📝 Notes",
    placeholder="Enter what you want to learn..."
)

status = st.selectbox(
    "📌 Learning Status",
    ["Not Started", "Learning", "Revision", "Completed"]
)

target_date = st.date_input(
    "🎯 Target Completion Date",
    min_value=date.today()
)

if st.button("Add Topic"):
    if topic_name:

        completed = True if status == "Completed" else False

        st.session_state.topics.append({
            "topic": topic_name,
            "notes": notes,
            "status": status,
            "target_date": target_date,
            "completed": completed
        })

        st.success(f"✅ {topic_name} added successfully!")

    else:
        st.warning("⚠️ Please enter a topic name.")

st.divider()

# -----------------------------
# Display Topics
# -----------------------------
st.header("📚 My Learning Topics")

completed_count = 0

for i, topic in enumerate(st.session_state.topics):

    with st.container():

        col1, col2 = st.columns([5, 1])

        with col1:

            completed = st.checkbox(
                f"**{topic['topic']}**",
                value=topic["completed"],
                key=f"check_{i}"
            )

            st.session_state.topics[i]["completed"] = completed

            if completed:
                completed_count += 1

            st.write(f"📝 Notes: {topic['notes']}")

            st.write(f"📌 Status: {topic['status']}")

            st.write(
                f"🎯 Target Date: {topic['target_date']}"
            )

            days_left = (
                topic["target_date"] - date.today()
            ).days

            if completed:
                st.success("✅ Topic Completed")

            else:
                if days_left >= 0:
                    st.info(
                        f"⏳ {days_left} day(s) remaining"
                    )
                else:
                    st.error(
                        f"⚠️ Deadline missed by {-days_left} day(s)"
                    )

        with col2:

            if st.button(
                "🗑 Delete",
                key=f"delete_{i}"
            ):
                st.session_state.topics.pop(i)
                st.rerun()

        st.divider()

# -----------------------------
# Progress Dashboard
# -----------------------------
total_topics = len(st.session_state.topics)

if total_topics > 0:

    progress = completed_count / total_topics

    st.header("📊 Progress Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "📚 Total Topics",
        total_topics
    )

    col2.metric(
        "✅ Completed",
        completed_count
    )

    col3.metric(
        "⏳ Pending",
        total_topics - completed_count
    )

    st.progress(progress)

    st.write(
        f"### Overall Progress: {progress*100:.1f}%"
    )

    if progress == 1:
        st.balloons()
        st.success(
            "🎉 Congratulations! All topics completed!"
        )

else:
    st.info("📌 No topics added yet.")