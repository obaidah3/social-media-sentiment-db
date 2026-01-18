import streamlit as st

from queries.users import (
    all_users,
    users_with_no_posts,
    recent_users,
    dark_theme_users
)

from queries.posts import (
    all_posts,
    posts_by_visibility
)

from queries.engagement import most_engaging_posts
from queries.sentiment import comment_sentiments
from queries.social import followed_users_by_id
# from queries.analytics import notifications_by_user_id
from queries.analytics import post_count_per_user, notifications_by_user_id


st.set_page_config(page_title="SQL Dashboard", layout="wide")
st.title("🗄️ Social Media SQL Dashboard")

menu = st.sidebar.radio(
    "Query Category",
    [
        "Users",
        "Posts",
        "Engagement",
        "Sentiment",
        "Social",
        "Analytics"
    ]
)

def show(df, title):
    st.subheader(title)
    st.dataframe(df, use_container_width=True)

if menu == "Users":

    if st.button("👤 All Users"):
        show(all_users(), "All Users")

    if st.button("🚫 Users With No Posts"):
        show(users_with_no_posts(), "Users With No Posts")

    if st.button("🆕 Recent Users"):
        show(recent_users(), "Users Joined Recently")

    if st.button("🌙 Dark Theme Users"):
        show(dark_theme_users(), "Users With Dark Theme")

elif menu == "Posts":

    if st.button("📝 All Posts"):
        show(all_posts(), "All Posts")

    if st.button("👁️ Posts by Visibility"):
        show(posts_by_visibility(), "Posts by Visibility")

elif menu == "Engagement":

    if st.button("🔥 Most Engaging Posts"):
        show(most_engaging_posts(), "Most Engaging Posts")


elif menu == "Sentiment":

    if st.button("🧠 Comment Sentiments"):
        show(comment_sentiments(), "Comment Sentiments")


elif menu == "Social":

    user_id = st.number_input(
        "Enter User ID",
        min_value=1,
        step=1
    )

    if st.button("👥 Users Followed by This User"):
        show(
            followed_users_by_id(user_id),
            f"Users Followed by User ID {user_id}"
        )

elif menu == "Analytics":

    if st.button("📊 Post Count per User"):
        show(post_count_per_user(), "Post Count per User")

    user_id = st.number_input(
        "Enter User ID",
        min_value=1,
        step=1,
        key="notif_id"
    )

    if st.button("🔔 Notifications for This User"):
        show(
            notifications_by_user_id(user_id),
            f"Notifications for User ID {user_id}"
        )
