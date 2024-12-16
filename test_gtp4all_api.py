import requests
import re
import json

# Define the API endpoint
url = "http://localhost:4891/v1/chat/completions"  # Replace with your GPT4All HTTP API endpoint

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
"""

# Define the request payload
payload= {
    "model": "Meta-Llama-3-8B-Instruct.Q4_0.gguf",  # Replace with your model name
    "messages": [
        {
            "role": "user",
            "content": prompt
        }
    ],
    "max_tokens": 2048
}

payload1={
    "model": "Meta-Llama-3-8B-Instruct.Q4_0.gguf",  # Replace with your model name
    "messages": [
        {
            "role": "user",
            "content": "${prompt}"
        }
    ],
    "max_tokens": 2048
}

# Send the POST request
print(payload1)
exit(0)

response = requests.post(url, json=payload)
if response.status_code == 200:
    message= response.json()["choices"][0]["message"]["content"]

    # Regular expression to capture the JSON portion
    json_pattern = r"\{.*\}"

    # Extract JSON string
    json_match = re.search(json_pattern, message, re.DOTALL)
    if json_match:
        json_string = json_match.group(0)

        # Clean up the JSON string (remove comments)
        json_string = re.sub(r"//.*", "", json_string)

        try:
            # Load JSON
            json_data = json.loads(json_string)
            for key,values in json_data.items():
                print(f"{key}: {values}")
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
    else:
        print("No JSON found in the string.")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
