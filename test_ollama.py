from ollama import chat
from ollama import ChatResponse


# Define the email and JSON message format
email = """
Dear Marriot Hotel,

I would like to reserve a two bedroom with twin bed in each room for 2 days 1 night with breakfast on November 10. Could I have a room with balcony? 

I take first flight so I will arrive at the hotel around 10 a.m. if it possible, could I get early check in? Also, I need fast Wifi connection because I have a few things to work on evening. 

I have promotional code(defdet55%). Please can you give me the room rate tomorrow and do you accept credit card? Do the room is already breakfast included?


Please let me know if you need further information.


Kindly Regards,

George
"""

json_message = """
{
    "questions": string,
    "payment_method": string,
    "promotional_code": string,
    "total_number_of_beds": 0,
    "total_number_of_guests": 0,
    "guest_distribution": [
        {
            "room_type": "string",
            "number_of_guests": 0
        }
    ],
    "special_requests": [
        "string"
    ],
    "number_of_rooms": 0,
    "checkin_date": "YYYY-MM-DD",
    "checkout_date": "YYYY-MM-DD"
}
"""

# Define the prompt
prompt = f"""
Extract from the email the following and return a strucutred  output in json format with this specification:
{json_message}
{email}
The possible room configurations are:
room type 1: 2 bedrooms with 2 twin beds each
room type 2: 1 bedrooms with 1 twin bed each
room type 3: 1 bedrooms with 1 single bed each
you should match the number of guests to the room configuration.
"""


response: ChatResponse = chat(model='llama3.2', messages=[
  {
    'role': 'user',
    'content': prompt,
  },
])
print(response['message']['content'])
# or access fields directly from the response object
print(response.message.content)