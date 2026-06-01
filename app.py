import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns

st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="💬",
    layout="wide",
)

st.markdown(
    "<div style='text-align: center; margin-bottom: 1.5rem;'>"
    "<h1 style='margin: 0;'>WhatsApp Chat Analyzer</h1>"
    "<p style='margin: 0.25rem 0 0; color: red;'>Upload your WhatsApp export file(s) and explore message trends, engagement, and emoji usage.</p>"
    "</div>",
    unsafe_allow_html=True,
)

st.sidebar.title("Upload WhatsApp Chat Export")
st.sidebar.info(
    "Upload one or more WhatsApp export files and view analysis for the entire chat or a specific participant."
)
st.sidebar.markdown("---")

uploaded_files = st.sidebar.file_uploader("Choose file(s)", type=["txt", "log"], accept_multiple_files=True)

if uploaded_files:
    all_data = []
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.getvalue()
        decoded = None
        for encoding in ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1']:
            try:
                decoded = bytes_data.decode(encoding)
                break
            except UnicodeDecodeError:
                continue
        if decoded is None:
            st.error(f"Unable to decode {uploaded_file.name}. Please upload a valid text file.")
            continue
        all_data.append(decoded)

    if not all_data:
        st.stop()

    data = "\n".join(all_data)
    df = preprocessor.preprocess(data)

    if df.empty:
        st.error("No valid messages found in the uploaded file(s).")
        st.stop()

    user_list = sorted([user for user in df['user'].unique() if user != 'group_notification'])
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Tip:** Select `Overall` for full chat analysis, or choose a user to see individual performance.")

    num_messages, words, num_media_messages, num_links = helper.fetch_status(selected_user, df)
    st.header("Top Statistics")
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Messages", value=num_messages)
    with col2:
        st.metric(label="Total Words", value=words)
    with col3:
        st.metric(label="Media Shared", value=num_media_messages)
    with col4:
        st.metric(label="Links Shared", value=num_links)

    st.markdown("---")
    st.header("Monthly Timeline")
    timeline = helper.monthly_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(timeline['time'], timeline['messages'], color='green')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

## Daily Timeline
    st.header("Daily Timeline")
    daily_timeline = helper.daily_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(daily_timeline['only_date'], daily_timeline['messages'], color='blue')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    st.markdown("---")
    st.header("Weekly Activity Map")
    col1,col2 = st.columns(2)
    with col1:
        st.header("Most Busy Day")
        busy_day = helper.weekly_activity_map(selected_user, df)
        fig,ax = plt.subplots()
        ax.bar(busy_day.index, busy_day.values)
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
    with col2:
        st.header("Most Busy Month")
        busy_month = helper.monthly_activity_map(selected_user, df)
        fig,ax = plt.subplots()
        ax.bar(busy_month.index, busy_month.values, color = 'orange')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
    
    st.markdown("---")
    st.header("Daywise Activity HeatMap")
    user_heatmap = helper.activity_heatmap(selected_user, df)
    fig,ax = plt.subplots()
    ax = sns.heatmap(user_heatmap)
    st.pyplot(fig)

    st.markdown("---")
    if selected_user == 'Overall':
        st.header("Most Busy Users")
        x, new_df = helper.most_busy_users(df)
        fig, ax = plt.subplots()
        col1, col2 = st.columns(2)
        with col1:
            ax.bar(x.index, x.values, color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.dataframe(new_df)
## Word Cloud
    st.header("Word Cloud")
    df_wc = helper.create_wordcloud(selected_user, df)
    fig, ax = plt.subplots()
    ax.imshow(df_wc, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)
## Emoji Analysis
    st.header("Emoji Analysis")
    emoji_df = helper.emoji_helper(selected_user, df)
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(emoji_df)
    with col2:
        fig, ax = plt.subplots()
        if not emoji_df.empty:
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)
        else:
            st.write("No emojis found in the selected data.")
