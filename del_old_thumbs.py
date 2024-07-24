import mysql.connector
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
import os

# Database connection parameters
db_config = {
    'user': os.environ.get("importDbUser"),
    'password': os.environ.get("importDbPassword"),
    'host': os.environ.get("importDbHost"),
    'database': os.environ.get("importDbName"),
}

def delete_value(thumbnail):
    # print('Attempting to connect to the database...')
    # Connect to the database
    try:
        cnx = mysql.connector.connect(**db_config)
        # print('Connected to the database successfully.')
    except mysql.connector.Error as err:
        # print(f"Error connecting to the database: {err}")
        return
    
    cursor = cnx.cursor()

    try:
        # Perform delete operation
        query = "DELETE FROM catalog_product_entity_media_gallery WHERE value = %s"
        cursor.execute(query, (thumbnail,))
        cnx.commit()
        print(f"Deleted rows with value: {thumbnail}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        cnx.rollback()
    finally:
        cursor.close()
        cnx.close()

# Load CSV file
df = pd.read_csv('videos.csv', quotechar='"', lineterminator='\n')

# Handle NaN values by replacing them with empty strings or appropriate default values
df.fillna('', inplace=True)

# Iterate over each row in the CSV
for index, row in df.iterrows():
    thumbnail = row['thumbnail']
    if thumbnail != '':
        delete_value(thumbnail)
