import re
import pandas as pd
def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({"user_messages": messages, "message_date": dates})
    df['message_date'] = df['message_date'].str.replace(' - ', '')
    df['message_date'] = pd.to_datetime(df['message_date'], format = '%d/%m/%Y, %H:%M')
    df.rename(columns = {'message_date' : 'date'}, inplace = True)
    #seperate users and messages from user_messages
    users = []
    messages = []

    for msg in df['user_messages']:
        entry = re.split(r"([\w\W]+?):\s", msg) #"Swarnendu: Hello" -> ["", "Swarnendu", "Hello"]

        if entry[1:]:  # username exists because some were group notifications
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append("group_notification")
            messages.append(entry[0])

    df["user"] = users
    df["messages"] = messages
    df.drop(columns=["user_messages"], inplace=True)
    df['year'] = df['date'].dt.year
    df["month"] = df["date"].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df["day"] = df["date"].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df["hour"] = df["date"].dt.hour
    df["min"] = df["date"].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str(hour) + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['period'] = period

    return df
