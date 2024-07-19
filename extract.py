import mysql.connector
import csv
from dotenv import load_dotenv
load_dotenv()
import os

# Database connection parameters for the old Magento 2 database
db_config = {
    'user': os.environ.get("extractDbUser"),
    'password': os.environ.get("extractDbPassword"),
    'host': os.environ.get("extractDbHost"),
    'database': os.environ.get("extractDbName"),
}

# Function to extract video data from the old Magento 2 database
def extract_video_data():
    # Connect to the old database
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()

    # Adjusted query to get the SKU and video URL from the old database
    query = """
    SELECT
        cpe.sku,
        cpemgv.url AS video_url,
        cpemg.value AS thumbnail,
        cpemgv.title AS video_title,
        cpemgv.description AS video_description
    FROM
        catalog_product_entity cpe
    JOIN
        catalog_product_entity_media_gallery_value_to_entity cpemgvt ON cpe.entity_id = cpemgvt.entity_id
    JOIN
        catalog_product_entity_media_gallery cpemg ON cpemgvt.value_id = cpemg.value_id
    JOIN
        catalog_product_entity_media_gallery_value_video cpemgv ON cpemg.value_id = cpemgv.value_id
    WHERE
        cpemg.media_type = 'external-video';
    """

    try:
        cursor.execute(query)

        # Fetch all the results
        rows = cursor.fetchall()

        # Define the CSV file name
        csv_file = 'videos.csv'

        # Write the results to a CSV file
        with open(csv_file, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            # Write the header
            csvwriter.writerow(['sku', 'video_url', 'thumbnail', 'video_title', 'video_description'])
            # Write the data rows
            csvwriter.writerows(rows)

        print(f"Data extracted to {csv_file}")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()
        cnx.close()

# Run the function to extract and save the video data
extract_video_data()
