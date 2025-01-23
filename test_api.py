import requests
from datetime import datetime, timedelta
import random
from module import app_logging
import os
import json
import pandas as pd

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
    start_date = datetime.strptime(start_date_str, "%m/%d/%Y")
    end_date = datetime.strptime(end_date_str, "%m/%d/%Y")

    # Generate a random datetime between the two
    random_datetime = start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))

    # Split into separate date and time
    random_date = random_datetime.strftime("%m/%d/%Y")  # Format as 'YYYY-MM-DD'
    random_time = random_datetime.strftime("%H:%M:%S")  # Format as 'HH:MM:SS'
    
    return random_date, random_time



def read_text_files(directory):
    df = pd.DataFrame()    
    try:
        # List all files in the directory
        files = [f for f in os.listdir(directory) if f.endswith('.txt')]

        if not files:
            print("No .txt files found in the directory.")
            return

        for file in files:
            file_path = os.path.join(directory, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                print(f"Reading file: {file}")
                email = f.read()
                random_date, random_time = generate_random_date_and_time("01/01/2024", "12/31/2025")
                payload = {
                    "payload":{
                    "message": email,
                    "email_address": "john.doe@mail.com",
                    "subject":"Room Reservation request",
                    "date": f"{random_date} {random_time}"
                    }
                }
                headers = {
                    "Content-Type": "application/json"
                }

                response = requests.post(url, json=payload,headers=headers)
                       
                parsed_data = json.loads(response.text)

                message = parsed_data.get("message", {})

                success = parsed_data.get("success", False)

                row_data = {
                    "checkin_date": message.get("checkin_date", ""),
                    "checkout_date": message.get("checkout_date", ""),
                    "number_of_rooms": message.get("number_of_rooms", 0),
                    "payment_method": message.get("payment_method", ""),
                    "promotional_code": message.get("promotional_code", ""),
                    "total_number_of_beds": message.get("total_number_of_beds", 0),
                    "total_number_of_guests": message.get("total_number_of_guests", 0),
                    "visitor_name": message.get("visitor_name", ""),
                    "message": email
                }

                guest_distribution = message.get("guest_distribution", [])
                special_requests = message.get("special_requests", [])

                guest_rows = []

                for guest in guest_distribution:
                    guest_row = row_data.copy()  # Copy base data for each guest
                    guest_row["room_type"] = guest.get("room_type", "")
                    guest_row["number_of_guests"] = guest.get("number_of_guests", 0)
                    guest_rows.append(guest_row)

                for special_request in special_requests:
                    guest_row = row_data.copy()  # Copy base data for each special request
                    guest_row["special_request"] = special_request.get("request","")
                    guest_rows.append(guest_row)

                df = pd.concat([df, pd.DataFrame(guest_rows)], ignore_index=True)
        df.to_excel("test_output.xlsx", index=False)
    except Exception as e:
        print(f"An error occurred: {e}")




# Directory containing .txt files
directory_path = "C:/Users/georg/Python Projects/HotelBooking/emails"
read_text_files(directory_path)

