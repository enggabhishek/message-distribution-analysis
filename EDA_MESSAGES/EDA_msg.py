# Import python packages
import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import snowflake.connector
import os
# session = get_active_session()
from dotenv import load_dotenv
load_dotenv()

# print(os.getenv('USERNAME_2'))
# print(os.getenv('SNOWSQL_PWD'))
# print(os.getenv('ACCOUNT_NAME'))
# print(os.getenv('DATABASE'))
# print(os.getenv('SCHEMA'))
# print(os.getenv('WAREHOUSE'))
conn = snowflake.connector.connect(
    user=os.getenv('USERNAME_2'),
    password=os.getenv('SNOWSQL_PWD'),
    account=os.getenv('ACCOUNT_NAME'),
    database=os.getenv('DATABASE'),
    schema=os.getenv('SCHEMA'),
    warehouse=os.getenv('WAREHOUSE'),
    login_timeout=60,
    client_session_keep_alive=True 
)

cursor = conn.cursor()
query = 'Select message_type from message_tbl where message_type IS NOT NULL'
cursor.execute(query)
result = cursor.fetchall()

message_type_df = pd.DataFrame(result, columns=[col[0] for col in cursor.description])

# Assuming you have a DataFrame named 'messages_df' with a column named 'message_type'
plt.figure(figsize=(8, 6))
ax = sns.countplot(x='MESSAGE_TYPE', data=message_type_df)
plt.title('Count of Messages by Message Type')
plt.xlabel('Message Type')
plt.ylabel('Count')
# plt.show()
st.pyplot(plt)