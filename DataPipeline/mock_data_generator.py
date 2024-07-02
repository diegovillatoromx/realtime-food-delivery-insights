import pandas as pd
import json
import random
from datetime import datetime
from faker import Faker
import boto3
import os
import time

# Initialize Faker and Boto3 Kinesis client
fake = Faker()
kinesis_client = boto3.client('kinesis')

# Directory setup
base_directory = os.path.dirname(__file__)
data_directory = os.path.join(base_directory, "data_for_dims")

def load_ids_from_csv(file_name, key_attribute):
    """Load IDs from the specified CSV file within the data directory."""
    file_path = os.path.join(data_directory, file_name)
    df = pd.read_csv(file_path)
    return df[key_attribute].tolist()

def generate_order(customer_ids, restaurant_ids, rider_ids, order_id):
    """Generate a mock order record."""
    order = {
        'OrderID': order_id,
        'CustomerID': random.choice(customer_ids),
        'RestaurantID': random.choice(restaurant_ids),
        'RiderID': random.choice(rider_ids),
        'OrderDate': fake.date_time_between(start_date='-30d', end_date='now').isoformat(),
        'DeliveryTime': random.randint(15, 60),  # Delivery time in minutes
        'OrderValue': round(random.uniform(10, 100), 2),
        'DeliveryFee': round(random.uniform(2, 10), 2),
        'TipAmount': round(random.uniform(0, 20), 2),
        'OrderStatus': random.choice(['Delivered', 'Cancelled', 'Processing', 'On the way'])
    }
    return order

def send_order_to_kinesis(stream_name, order):
    """Send the generated order to a Kinesis stream."""
    response = kinesis_client.put_record(
        StreamName=stream_name,
        Data=json.dumps(order),
        PartitionKey=str(order['OrderID'])  # Using OrderID as the partition key
    )
    print(f"Sent order to Kinesis with Sequence Number: {response['SequenceNumber']}")

# Load mock data IDs
customer_ids = load_ids_from_csv('dimCustomers.csv', 'CustomerID')
restaurant_ids = load_ids_from_csv('dimRestaurants.csv', 'RestaurantID')
rider_ids = load_ids_from_csv('dimDeliveryRiders.csv', 'RiderID')

# Kinesis Stream Name
stream_name = 'incoming-food-order-data'

# Order ID initialization
order_id = 5000

for _ in range(1000):
    order = generate_order(customer_ids, restaurant_ids, rider_ids, order_id)
    print(order)
    send_order_to_kinesis(stream_name, order)
    order_id += 1  # Increment OrderID for the next order