from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extractor = URLExtract()
def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]

    num_messages = df.shape[0]
    words = [word for sent in df['messages'] for word in sent.split()]
    #Fetch number of media messages
    num_media_msgs = df[df['messages'] == "<Media omitted>\n"].shape[0]
    #fetch number of links 
    links = [link for message in df.messages for link in extractor.find_urls(message)]

    return num_messages, len(words), num_media_msgs, len(links)

def most_busy_users(df):
    x = df.user.value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name', 'user':'percent'})
    return x, df

def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user] 
    temp = df[df['user'] !='Group Notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']
    with open('stopwords.txt', 'r') as f:
        stop_words = f.read()
    wc = WordCloud(width=500, height=500, min_font_size = 10, background_color= 'white')
    wc_data = [word for message in temp['messages'] for word in message.lower().split() if word not in stop_words]
    #df_wc = wc.generate(temp['messages'].str.cat(sep=' '))
    wc_data = ' '.join(wc_data)
    return wc_data

def most_common_words(selected_user, df):
    with open('stopwords.txt', 'r') as f:
        stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]

    temp = df[df['user'] !='Group Notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']
    words = [word for message in temp.messages for word in message.lower().split() if word not in stop_words]
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    emojis = [c for message in df['messages'] for c in message if c in emoji.UNICODE_EMOJI['en']]
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['messages'].reset_index()
    timeline['time'] = ['-'.join(i) for i in zip(timeline["month"],timeline["year"].map(str))]
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    daily_timeline = df.groupby(by='date').count()['messages'].reset_index()
    return daily_timeline

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    return df.day_name.value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    return df.month.value_counts() 

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    user_heatmap = df.sort_values(by = 'hour', ascending=True).pivot_table(index='day_name',
                                         columns='period', values='messages', aggfunc='count').fillna(0)
    return user_heatmap