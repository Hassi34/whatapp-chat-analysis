import re
import pandas as pd 
def preprocess(data):
    pattern = "\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s\w[a-zA-Z]\s-\s"
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_message':messages, 'date_time': dates})
    df['date_time'] = df.date_time.apply(lambda x: x[:-3])
    df['date'] = (df.date_time.str.split(",").str[0])
    df['time'] = (df.date_time.str.split(",").str[1]).apply(lambda x: x.strip())
    users = []
    messages = []
    for message in df.user_message:
        entry = re.split('([\w\W)]+?):\s', message)
        if entry[1:]: #user_name
            users.append(entry[1])
            messages.append(entry[2])
        else :
            users.append('Group Notification')
            messages.append(entry[0])
    df['user'] = users
    df['messages'] = messages
    df['year'] = pd.to_datetime(df['date']).dt.year
    df['month'] = pd.to_datetime(df['date']).dt.month_name()
    df['month_num'] = pd.to_datetime(df['date']).dt.month
    df['day_name'] = pd.to_datetime(df['date']).dt.day_name()
    df['day'] = pd.to_datetime(df.date).dt.day
    df['hour'] = pd.to_datetime(df.time).dt.hour
    df['minute'] = pd.to_datetime(df.time).dt.minute
    df.drop(columns=['user_message','date_time'], inplace=True)

    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour+1))
        else:
            period.append(str(hour) + "-" + str(hour+1))
    df['period'] = period 

    return df