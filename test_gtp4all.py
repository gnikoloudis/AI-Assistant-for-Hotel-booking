from gpt4all import GPT4All
model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf",device="cuda") # downloads / loads a 4.66GB LLM
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
                        "questions": string,  // Integer: Total number of guests
                        "payment_method": string,  // Integer: Total number of guests
                        "promotinal_code": string,  // Integer: Total number of guests
                        "total_number_of_beds": 0,  // Integer: Total number of guests
                        "total_number_of_guests": 0,  // Integer: Total number of guests
                        "guest_distribution": [       // Array of objects: Details per room type
                            {
                                "room_type": "string",        // String: Type of room (e.g., "Deluxe Suite")
                                "number_of_guests": 0        // Integer: Number of guests in this room type
                            }
                        ],
                        "special_requests": [         // Array of strings: Any special requests
                            "string"
                        ],
                        "number_of_rooms": 0,         // Integer: Total number of rooms booked
                        "checkin_date": "YYYY-MM-DD", // String: Check-in date in ISO format
                        "checkout_date": "YYYY-MM-DD" // String: Check-out date in ISO format
                    }
"""
with model.chat_session():
    print(model.generate(f"""
                         Extract from the email the following and return the output in a json format with this specification.
                         {json_message}
                         {email}
                         
                         """, 
                         max_tokens=2048))
    