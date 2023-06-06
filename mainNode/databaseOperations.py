import psycopg2
import logging

logging.basicConfig(level=logging.INFO)

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    database="frames_get",
    user="postgres",
    password="root",
    host="localhost",
    port="5432",
)

def store_processed_frames(task_id, frame_id, time_taken, worker_id, frame_data):
    try:
        connection = psycopg2.connect(
            database="frames_get",
            user="postgres",
            password="root",
            host="localhost",
            port="5432")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO frames(task_id,frame_id,time_taken, woker_id, image) VALUES (%s,%s, %s, %s, %s)", (1,frame_id, time_taken, worker_id, frame_data))
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        logging.info("Failed to insert processed frame into database", error)
    finally:
    # closing database connection.
        if connection:
            cursor.close()
            connection.close()