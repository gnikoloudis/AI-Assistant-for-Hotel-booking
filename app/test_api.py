import requests
from datetime import datetime, timedelta
import random
from module import app_logging
import os

url = "http://127.0.0.1:5000/read-email"

def generate_random_date_and_time(start_date_str, end_date_str):
    """
    Generate a random date and time between two provided dates.

    Args:
        start_date_str (str): Start date in the format 'YYYY-MM-DD'.
        end_date_str (str): End date in the format 'YYYY-MM-DD'.

    Returns:
        tuple: A tuple containing the random date and time as separate variables.
    """
    # Convert string arguments to datetime objects
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    # Generate a random datetime between the two
    random_datetime = start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))

    # Split into separate date and time
    random_date = random_datetime.strftime("%Y-%m-%d")  # Format as 'YYYY-MM-DD'
    random_time = random_datetime.strftime("%H:%M:%S")  # Format as 'HH:MM:SS'
    
    return random_date, random_time



def read_text_files(directory):
    try:
        # List all files in the directory
        files = [f for f in os.listdir(directory) if f.endswith('.txt')]

        if not files:
            print("No .txt files found in the directory.")
            return

        for file in files[:1]:
            file_path = os.path.join(directory, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                print(f"Reading file: {file}")
                message = f.read()
                random_date, random_time = generate_random_date_and_time("2025-11-01", "2025-12-31")
                payload = {
                    "payload":{
                    "message": message,
                    "email_address": "john.doe@mail.com",
                    "subject":"Room Reservation request",
                    "date": random_date,
                    "time": random_time
                    }
                }

                response = requests.post(url, json=payload)
                #message= response.json()["choices"][0]["message"]["content"]
                print(response)
    
    except Exception as e:
        print(f"An error occurred: {e}")




# Directory containing .txt files
directory_path = "C:/Users/georg/Python Projects/HotelBooking/emails"
read_text_files(directory_path)
