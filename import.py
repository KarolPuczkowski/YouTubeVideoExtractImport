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

# Function to insert video data into Magento 2 database
def insert_video_data(sku, video_url, thumbnail, video_title, video_description):
    # Connect to the database
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()

    # Get product ID by SKU
    cursor.execute("SELECT entity_id FROM catalog_product_entity WHERE sku = %s", (sku,))
    result = cursor.fetchone()
    if not result:
        print(f"Product with SKU {sku} not found.")
        return

    product_id = result[0]
    print("Product ID:")
    print(product_id)

    # Insert video data into the database
    try:
        # Insert into catalog_product_entity_media_gallery
        cursor.execute("""
            INSERT INTO catalog_product_entity_media_gallery
            (attribute_id, value, media_type, disabled)
            VALUES
            ((SELECT attribute_id FROM eav_attribute WHERE attribute_code = 'media_gallery'), %s, 'external-video', 0)
        """, (thumbnail,))
        media_gallery_id = cursor.lastrowid
        print("Media Gallery ID:")
        print(media_gallery_id)

        # Insert into catalog_product_entity_media_gallery_value
        cursor.execute("""
            INSERT INTO catalog_product_entity_media_gallery_value
            (value_id, store_id, entity_id, position, disabled)
            VALUES
            (%s, 0, %s, 0, 0)
        """, (media_gallery_id, product_id))

        value_id = media_gallery_id  # Use the same media_gallery_id as value_id
        print("Value ID:")
        print(value_id)

        # Insert into catalog_product_entity_media_gallery_value_video
        cursor.execute("""
            INSERT INTO catalog_product_entity_media_gallery_value_video
            (value_id, title, description, url, metadata)
            VALUES
            (%s, %s, %s, %s, '')
        """, (value_id, video_title, video_description, video_url))

        # Insert into catalog_product_entity_media_gallery_value_to_entity
        cursor.execute("""
            INSERT INTO catalog_product_entity_media_gallery_value_to_entity
            (value_id, entity_id)
            VALUES
            (%s, %s)
        """, (value_id, product_id))

        cnx.commit()
        print(f"Video for SKU {sku} inserted successfully.")

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
    sku = row['sku']
    video_url = row['video_url']
    thumbnail = row['thumbnail']
    video_title = row['video_title']
    video_description = row['video_description']

    # Insert video data into Magento 2 database
    insert_video_data(sku, video_url, thumbnail, video_title, video_description)
