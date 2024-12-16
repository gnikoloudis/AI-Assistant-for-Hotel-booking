import json
from module import app_logging
import requests
from pydantic import BaseModel
from  datetime import date,datetime

url = "http://localhost:11434/api/generate"


class GuestDistribution(BaseModel):
    room_type: str
    number_of_guests: int

class SpecialRequests(BaseModel):
    request: str

class Reservation(BaseModel):
    payment_method: str
    promotional_code: str
    total_number_of_beds:int
    total_number_of_guests:int
    guest_distribution: list[GuestDistribution]
    special_requests:list[SpecialRequests]
    number_of_rooms:int
    checkin_date:date
    checkout_date:date
    visitor_name:str

def send_to_llm(message,language,date):
    

    headers = {
        "Content-Type": "application/json"
    }
    
    now = datetime.today().strftime('%Y-%m-%d')

    prompt = f"""
    The language of the request is {language} 
    If the complete checkin date is not provided then assume the checkin date to be {now}.

    The possible room configurations you can offer are:
        Room type 1: 2 bedrooms with 2 twin beds each
        Room type 2: 1 bedrooms with 1 twin bed each
        Room type 3: 1 bedrooms with 1 single bed each
    You should match the number of guests to the room configuration.
    Extract the required information from the email and return the respose to JSON.
    Below is the email message from the customer.
    {message}
    """
    
    data = {
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False,
        "format": Reservation.model_json_schema(),
        "options": {
            "temperature": 0.2,
            "top_p": 0.5,
            "top_k": 40,
            "max_tokens": 10000
        }
    }

    try:
        # Make the POST request
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        if response.status_code == 200:
            return(json.loads(response.json()['response']))
    except requests.exceptions.RequestException as e:
        app_logging.error(f"Error in LLM request: {e.with_traceback}")
        return None     