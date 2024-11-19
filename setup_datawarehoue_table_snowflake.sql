-- Step 1: Create Storage Integration
CREATE OR REPLACE STORAGE INTEGRATION my_azure_integration
TYPE = EXTERNAL_STAGE
STORAGE_PROVIDER = 'AZURE'
ENABLED = TRUE
AZURE_TENANT_ID = '<TENANT ID>'
STORAGE_ALLOWED_LOCATIONS = ('<Azure Blob Storage Container URL>');

-- Step 2: Retrieve Storage Integration Info
DESC STORAGE INTEGRATION my_azure_integration;

-- Step 3: Create Stage
CREATE OR REPLACE STAGE my_stage
URL = '<Azure Blob Storage Container URL>'
STORAGE_INTEGRATION = my_azure_integration;


CREATE OR REPLACE TEMP  FILE FORMAT my_csv_format
   TYPE =  CSV
   COMPRESSION = AUTO 

CREATE OR REPLACE STAGE my_stage
  URL='<Azure Blob Storage Container URL>'
  CREDENTIALS=(AZURE_SAS_TOKEN='<Azure Blob Storage SAS TOKE>')
  ENCRYPTION=(TYPE='AZURE_CSE' MASTER_KEY = '<ENTER YOUR MASTER KEY>')
  FILE_FORMAT = my_csv_format;

ls @my_stage
-- Step 4: Create Table
CREATE OR REPLACE TABLE message_tbl (
    id VARCHAR,
    message_id VARCHAR,
    campaign_id NUMBER,
    message_type VARCHAR,
    client_id NUMBER(20,0),
    channel VARCHAR,
    category VARCHAR,
    platform VARCHAR,
    email_provider VARCHAR,
    streaming VARCHAR,
    dates DATE,
    sent_at TIMESTAMP,
    is_opened VARCHAR,
    opened_first_time_at TIMESTAMP,
    opened_last_time_at VARCHAR,
    is_clicked VARCHAR,
    clicked_first_time_at TIMESTAMP,
    clicked_last_time_at VARCHAR,
    is_unsubscribed VARCHAR,
    unsubscribed_at VARCHAR,
    is_hard_bounced VARCHAR,
    hard_bounced_at VARCHAR,
    is_soft_bounced VARCHAR,
    soft_bounced_at VARCHAR,
    is_complained VARCHAR,
    complained_at TIMESTAMP,
    is_blocked VARCHAR,
    blocked_at VARCHAR,
    is_purchased VARCHAR,
    purchased_at TIMESTAMP,
    created_at VARCHAR,
    updated_at VARCHAR
  -- Add other columns as per your CSV structure
);

DROP TABLE campaign_tbl
CREATE OR REPLACE TABLE campaign_tbl 
(
id Number,
campaign_type VARCHAR,
channel	VARCHAR,
topic	VARCHAR,
started_at	VARCHAR,
finished_at	TIMESTAMP,
total_count	NUMBER,
ab_test	VARCHAR(6),
warmup_mode	VARCHAR(6),
hour_limit	NUMBER,
subject_length	NUMBER,
subject_with_personalization VARCHAR(6),	
subject_with_deadline	VARCHAR(6),
subject_with_emoji	VARCHAR(6),
subject_with_bonuses	VARCHAR(6),
subject_with_discount VARCHAR(6),	
subject_with_saleout	VARCHAR(6),
is_test	VARCHAR(6),
positions VARCHAR(6)
);

-- Step 5: Copy Data into Table
COPY INTO campaign_tbl
FROM @my_stage/files/campaigns.csv
FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1) 
ON_ERROR = CONTINUE;


-- Step 5: Copy Data into Table
COPY INTO message_tbl
FROM @my_stage/files/messages.csv
FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1)
ON_ERROR = CONTINUE;



CREATE STREAMLIT hello_streamlit 
ROOT_LOCATION = '@<DB>.<Schema>.<Stage_Name>'
MAIN_FILE = '<Example.py file>'
QUERY_WAREHOUSE = compute_wh;

Select sent_at from message_tbl
limit 10;


UPDATE message_tbl
SET is_opened = CASE WHEN is_opened = 't' THEN TRUE ELSE FALSE END;


CREATE TABLE message_extended as 
Select m.*, cp.subject_with_bonuses, cp.subject_length, cp.subject_with_deadline, cp.subject_with_discount, cp.subject_with_emoji, cp.subject_with_saleout
from message_tbl as m
inner join campaign_tbl as cp
on m.campaign_id = cp.ID
where cp.campaign_type =  m.message_type;


