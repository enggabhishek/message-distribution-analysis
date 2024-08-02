import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
# We can also use Snowpark for our analyses!
from snowflake.snowpark.context import get_active_session
session = get_active_session()

message_type = session.sql("Select message_type from message_tbl where message_type IS NOT NULL")

message_type_df = message_type.to_pandas()

# Assuming you have a DataFrame named 'messages_df' with a column named 'message_type'
plt.figure(figsize=(8, 6))
ax = sns.countplot(x='MESSAGE_TYPE', data=message_type_df)
plt.title('Count of Messages by Message Type')
plt.xlabel('Message Type')
plt.ylabel('Count')

# Add count values inside the bars
for i, p in enumerate(ax.patches):
    ax.annotate(f'{p.get_height():.0f}', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 5),textcoords='offset points')
# plt.show()

st.pyplot(plt)

dates = session.sql("Select dates from message_tbl where dates IS NOT NULL")
messages_df = dates.to_pandas()
dtypes = {'DATES': 'datetime64[ns]'}
messages_df = messages_df.astype(dtypes)
plt.figure(figsize=(12, 6))
messages_by_day = messages_df.groupby(messages_df['DATES'].dt.date).size()
messages_by_day.plot(kind='line', marker='o', color='steelblue')
plt.title('Number of Messages Sent per Day', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.xticks(rotation=45, fontsize=10)
plt.yticks(fontsize=10)

plt.show()


channel = session.sql("Select channel from message_tbl where channel IS NOT NULL")
messages_df = channel.to_pandas()

plt.figure(figsize=(8, 8))
channel_counts = messages_df['CHANNEL'].value_counts()
colors = ['purple', 'darkgreen','yellow']

# Explode the largest slice
explode = [0.1 if i == channel_counts.idxmax() else 0 for i in channel_counts.index]

plt.pie(channel_counts, labels=channel_counts.index, autopct='%1.1f%%', startangle=90, colors=colors, wedgeprops={'edgecolor': 'white'})

plt.title('Distribution of Channels', fontsize=16, fontweight='bold')

# Equal aspect ratio ensures that pie is drawn as a circle
plt.axis('equal')

# plt.tight_layout()
centre_circle = plt.Circle((0, 0), 0.70, fc='white')
fig = plt.gcf()
 
# Adding Circle in Pie chart
fig.gca().add_artist(centre_circle)

plt.show()

sent_at=session.sql("Select sent_at from message_tbl where sent_at IS NOT NULL")
messages_df = sent_at.to_pandas()
dtypes = {'SENT_AT': 'datetime64[ns]'}
messages_df = messages_df.astype(dtypes)
plt.figure(figsize=(10, 6))
messages_df['SENT_AT_HOUR'] = messages_df['SENT_AT'].dt.hour

# Calculate the counts for each hour
hourly_counts = messages_df['SENT_AT_HOUR'].value_counts()

plt.hist(messages_df['SENT_AT_HOUR'], bins=24, color='steelblue', edgecolor='white')

plt.title('Distribution of Sent Time (Hourly)', fontsize=16, fontweight='bold')
plt.xlabel('Hour of the Day', fontsize=12)
plt.ylabel('Count', fontsize=12)

# Format y-axis labels in millions
plt.ticklabel_format(style='plain', axis='y', scilimits=(6, 6))
plt.gca().yaxis.get_major_formatter().set_scientific(False)

plt.xticks(range(0, 24))
plt.yticks(fontsize=10)

plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()

def time_periods(hour):
    if 0 <= hour < 6:
        return 'Night'
    elif 6 <= hour < 12:
        return 'Morning'
    elif 12 <= hour < 16:
        return 'Afternoon'
    else:
        return 'Evening'


 
#Apply the custom function to the 'hour' column and create a new 'period' column
messages_df['TimePeriod'] = messages_df['SENT_AT_HOUR'].apply(time_periods)


# Assuming you have a DataFrame named 'messages_df' with a column named 'TimePeriod'
plt.figure(figsize=(8, 8))
time_period_counts = messages_df['TimePeriod'].value_counts()

# Define custom colors for the pie chart
colors = ['steelblue', 'lightskyblue', 'lightcoral','orange']

plt.pie(time_period_counts, labels=time_period_counts.index, autopct='%1.1f%%', startangle=90,
        colors=colors, wedgeprops={'edgecolor': 'white'})

plt.title('Distribution of Time Periods', fontsize=16, fontweight='bold')
plt.axis('equal')

# Add a legend with custom colors and title
legend_labels = time_period_counts.index
plt.legend(legend_labels, title='Time Period', loc='best', bbox_to_anchor=(0.9, 0.9))

plt.tight_layout()
plt.show()