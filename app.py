import streamlit as st 
st.set_page_config(
page_title="Copyright © 2021 Hasnain",
page_icon="🎢",
layout="wide",
initial_sidebar_state="expanded")

import wordcloud
import preprocessor, helper
st.sidebar.title("Whatsapp Chat Analyzer")
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
from wordcloud import WordCloud
import seaborn as sns 

uploaded_file = st.sidebar.file_uploader("Choose a file")

st.sidebar.header('Get the Code')
link = '[GitHub](https://github.com/Hassi34/whatapp-chat-analysis.git)'
st.sidebar.markdown(link, unsafe_allow_html=True)

if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)

    #fetch unique users
    user_list = df.user.unique().tolist()
    user_list.remove('Group Notification')
    user_list.sort()
    user_list.insert(0, 'Overall')
    selected_user = st.sidebar.selectbox("Show Analysis w.r.t", user_list)
    helper.fetch_stats(selected_user, df)

    if st.sidebar.button("Show Analysis"):
        num_messages,words, num_media_msgs, num_links = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_msgs)
        with col4:
            st.header('Links Shared')
            st.title(num_links)
        
        #Monthly Timeline
        st.title('Monthly Timeline')
        timeline = helper.monthly_timeline(selected_user, df) 
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['messages'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        #Activity Map
        st.title('Activity Map')
        col1 , col2 = st.columns(2)
        with col1:
            st.header('Most Busy Days')
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation= 'vertical')
            st.pyplot(fig)  
        with col2:
            st.header('Most Busy Month')
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        #Finding the busiest users in the group(Group Level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                st.header('Count of messages')
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.header("Percentage of Messages")
                fig,ax = plt.subplots()
                new_df = new_df.sort_values(by='percent', ascending=True)
                ax.barh(new_df['name'][-14:],new_df['percent'][-14:])
                st.pyplot(fig)
                #st.dataframe(new_df)
        # WordCloud
        col1, col2 = st.columns(2)
        with col1:
            st.header("Wordcloud")
            wc_data = helper.create_wordcloud(selected_user, df)
            fig, ax = plt.subplots()
            wc_data = WordCloud(background_color='white').generate(wc_data)
            ax.imshow(wc_data)
            st.pyplot(fig)
        
        #Most Common Words
        with col2:
            st.header('Most Common Words')
            most_common_df = helper.most_common_words(selected_user, df)
            most_common_df = most_common_df.sort_values(by=1, ascending=True)
            fig, ax = plt.subplots()
            ax.barh(most_common_df[0], most_common_df[1])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        #Emoji Analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title('Emoji Analysis')
        col1, col2 = st.columns(2)
        with col1:
            st.header('Top 10 Emojis Used')
            fig, ax = plt.subplots()
            ax.bar(emoji_df[0][0:9], emoji_df[1][0:9])
            plt.xticks(rotation= 'vertical')
            st.pyplot(fig) 
        with col2:
            st.header("Percentage of Emjois Used")
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f%%")
            st.pyplot(fig)
        
        st.title('Weekly Activity Map')
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)