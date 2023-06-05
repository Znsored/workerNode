from confluent_kafka import Consumer
import base64
import logging
import json
import time
import numpy as np
import cv2

logging.basicConfig(level=logging.INFO)
def start_consuming():
    bootstrap_servers = "10.0.0.22:9093"
    logging.info(bootstrap_servers)

# Create consumer configuration
    consumer_config = {
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'my_consumer_2',
        'auto.offset.reset': 'earliest'
    }

# Create the Kafka consumer instance
    consumer = Consumer(consumer_config)

# Kafka topic to consume from
    topic = 'response'

# Subscribe to the Kafka topic
    consumer.subscribe([topic])

# Consume messages from the Kafka topic
    while True:
        logging.info("waiting for message")
        message = consumer.poll(1.0)

        if message is None:
            continue

        if message.error():
            logging.info(f"Consumer error: {message.error()}")
            continue

    # Decode the image from the message value
        logging.info("response received")
        json_message = message.value().decode('utf-8')
        try:
            job_data = json.loads(json_message)
        except json.JSONDecodeError as e:
        #print(f"Error decoding JSON message: {e}")
            continue
        frame_id = job_data['frame_id']
        image_base64 = job_data['image']
        worker_id = job_data['worker_id']
        time_taken = job_data['time_taken']

    # Decode the image from Base64
        image_data = base64.b64decode(image_base64)
        nparr = np.frombuffer(image_data, np.uint8)

# Decode the NumPy array to an OpenCV image
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

# Display the image
        cv2.imshow("Image", image)
        cv2.waitKey(0)
        
        logging.info(f"frame: {frame_id}, worker id: {worker_id}, time taken:{time_taken}")
        
    

    # Process the image data
    # ...

# Close the consumer
    consumer.close()
