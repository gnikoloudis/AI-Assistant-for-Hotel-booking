import random
from faker import Faker
import json
import inflect

# Initialize Faker and inflect
fake = Faker()
inflect_engine = inflect.engine()

# Define patterns for ROOM TYPE, GUEST TYPE, and greetings
room_types = ["Deluxe Suite", "Family Suite", "Standard Room", "Single Room", "Double Room", "Presidential Suite"]
guest_types = ["adults", "children", "infants"]
greetings = ["Greetings,", "Good morning,", "Good evening,", "Hi there,", "Hello,", "Dear Sir/Madam,", "To whom it may concern,","Hi,"]
closing_remarks = ["Thank you,", "Best regards,", "Sincerely,", "Looking forward to your response,", "Thanks in advance,", "Warm regards,"]
promo_codes = ["MH2219", "DISCOUNT10", "SPRING2024", "SUMMER22", "WINTER50"]
special_requests = [
    "Could I have a quiet room with a view if possible?",
    "Please ensure there is an iron and ironing board in the room.",
    "I would like extra pillows in the room.",
    "Could the room be on the top floor?",
    "Please provide a fruit basket in the room.",
    "I would like a room near the elevator.",
    "Could you arrange a late checkout?",
    "Please leave a bottle of water in the room."
]
prices = ["€80", "€90", "€100", "€120", "€150"]

# Helper function to convert numbers to words or digits
def get_number_variation(num):
    return inflect_engine.number_to_words(num)

# Generate annotated emails for NER
def generate_ner_training_data(num_examples=100):
    training_data = []
    for _ in range(num_examples):
        greeting = random.choice(greetings)
        closing = random.choice(closing_remarks)
        guest_name = fake.name()
        room_type = random.choice(room_types)
        num_guests = random.randint(1, 20)
        num_guests_text = get_number_variation(num_guests)
        guest_type = random.choice(guest_types)
        checkin_date = fake.date_between(start_date="today", end_date="+30d").strftime("%Y-%m-%d")
        checkout_date = fake.date_between(start_date="+31d", end_date="+60d").strftime("%Y-%m-%d")
        num_of_days = random.randint(1, 30)
        num_days_text = get_number_variation(num_of_days)
        num_of_rooms = random.randint(1, 5)
        num_of_rooms_text = get_number_variation(num_of_rooms)
        promo_code = random.choice(promo_codes)
        special_request = random.choice(special_requests)
        price_per_night = random.choice(prices)


        # Generate a random template
        templates_with_entities = [
            (f"{greeting} I would like to book a {room_type} for {num_guests_text} {guest_type}. Check-in date: {checkin_date}. Check-out date: {checkout_date}. {closing} {guest_name}",
             [("GUEST", guest_name), ("ROOM TYPE", room_type), ("NUMBER OF GUESTS", num_guests_text), ("GUEST TYPE", guest_type), ("CHECKIN DATE", checkin_date), ("CHECKOUT DATE", checkout_date)]),

            (f"{greeting} Could you please reserve a {room_type} for {num_guests_text} {guest_type}? Arrival date: {checkin_date}. Departure date: {checkout_date}. {closing} {guest_name}",
             [("GUEST", guest_name), ("ROOM TYPE", room_type), ("NUMBER OF GUESTS", num_guests_text), ("GUEST TYPE", guest_type), ("CHECKIN DATE", checkin_date), ("CHECKOUT DATE", checkout_date)]),
            

            (f"{greeting} I need accommodation in a {room_type} for {num_guests_text} {guest_type}, starting from {checkin_date} until {checkout_date}. {closing} {guest_name}",
             [("GUEST", guest_name), ("ROOM TYPE", room_type), ("NUMBER OF GUESTS", num_guests_text), ("GUEST TYPE", guest_type), ("CHECKIN DATE", checkin_date), ("CHECKOUT DATE", checkout_date)]),

            (f"{greeting} I would like to ask availability of a {num_of_rooms} room for {num_days_text} days checking on {checkin_date}. {closing} {guest_name}",
             [("GUEST", guest_name),  ("NUMBER OF ROOMS", num_of_rooms),("DAYS", num_days_text),("CHECKIN DATE", checkin_date)]),

            (f"{greeting} Could you please book a {room_type} for {num_guests_text} {guest_type}? We are planning to arrive on {checkin_date} and leave on {checkout_date}. {closing} {guest_name}",
             [("GUEST", guest_name),("ROOM TYPE", room_type), ("NUMBER OF GUESTS", num_guests_text),("GUEST TYPE", guest_type), ("CHECKIN DATE", checkin_date), ("CHECKOUT DATE", checkout_date)]),

            (f"{greeting} This is a request for booking a {room_type} for {num_guests_text} {guest_type}. Arrival date: {checkin_date}. Departure date: {checkout_date}. {closing} {guest_name}",
             [("GUEST", guest_name),("ROOM TYPE", room_type), ("NUMBER OF GUESTS", num_guests_text),("GUEST TYPE", guest_type),("CHECKIN DATE", checkin_date),  ("CHECKOUT DATE", checkout_date)]),

            (f"{greeting} I am interested in reserving a {room_type} for {num_guests_text} {guest_type}. The check-in is {checkin_date}, and the check-out is {checkout_date}. {closing} {guest_name}",
             [("GUEST", guest_name),("ROOM TYPE", room_type), ("NUMBER OF GUESTS", num_guests_text),("GUEST TYPE", guest_type),("CHECKIN DATE", checkin_date),  ("CHECKOUT DATE", checkout_date)]),

            (f"{greeting} I would like to inquire about the availability of a {room_type} for {num_guests_text} {guest_type} between {checkin_date} and {checkout_date}. {closing} {guest_name}",
             [("GUEST", guest_name),("ROOM TYPE", room_type), ("NUMBER OF GUESTS", num_guests_text),("GUEST TYPE", guest_type),("CHECKIN DATE", checkin_date),  ("CHECKOUT DATE", checkout_date)]),
             (
                f"Dear Ascot Hotel,\n"
                f"I would like to reserve a {room_type} for two nights with breakfast on {checkin_date} and {checkout_date}. "
                f"{special_request}\n"
                 f"Please could you confirm the booking? Let me know if you need any further information.\n"
                f"Many thanks.\n"
                f"With kind regards,\n"
                f"{guest_name}",
                [
                    ("ROOM TYPE", room_type),
                    ("CHECKIN DATE", checkin_date),
                    ("CHECKOUT DATE", checkout_date),
                    ("SPECIAL REQUEST", special_request),
                    ("GUEST", guest_name),
                ],
            ),
            (
                f"Hello Ascot Hotel,\n"
                f"I want to book a {room_type} for two nights from {checkin_date} to {checkout_date}. "
                f"{special_request}\n"
                f"My promo code is ({promo_code}). Is the rate still {price_per_night} per night with breakfast?\n"
                f"Please confirm my reservation at your earliest convenience.\n"
                f"Best regards,\n"
                f"{guest_name}",
                [
                    ("GUEST", guest_name),
                    ("ROOM TYPE", room_type),
                    ("CHECKIN DATE", checkin_date),
                    ("CHECKOUT DATE", checkout_date),
                    ("PROMOTIONAL CODE", promo_code),
                    ("PRICE PER NIGHT", price_per_night),
                    ("SPECIAL REQUEST", special_request),
                ],
            ),
            (
                f"Dear Team at Ascot Hotel,\n"
                f"I’d like to reserve a {room_type} for two nights with check-in on {checkin_date} and check-out on {checkout_date}. "
                f"{special_request}\n"
                f"I will use promo code ({promo_code}). Is the price {price_per_night} per night?\n"
                f"Kindly confirm the booking.\n"
                f"Sincerely,\n"
                f"{guest_name}",
                [
                    ("GUEST", guest_name),
                    ("ROOM TYPE", room_type),
                    ("CHECKIN DATE", checkin_date),
                    ("CHECKOUT DATE", checkout_date),
                    ("PROMOTIONAL CODE", promo_code),
                    ("PRICE PER NIGHT", price_per_night),
                    ("SPECIAL REQUEST", special_request),
                ],
            ),
            (
                f"Dear Ascot Hotel,\n"
                f"I’m looking to reserve a {room_type} for two nights, arriving on {checkin_date} and leaving on {checkout_date}. "
                f"{special_request}\n"
                f"I have a discount code ({promo_code}). Could you confirm if the cost is {price_per_night} per night?\n"
                f"Thank you in advance for confirming my reservation.\n"
                f"Yours sincerely,\n"
                f"{guest_name}",
                [
                    ("GUEST", guest_name),
                    ("ROOM TYPE", room_type),
                    ("CHECKIN DATE", checkin_date),
                    ("CHECKOUT DATE", checkout_date),
                    ("PROMOTIONAL CODE", promo_code),
                    ("PRICE PER NIGHT", price_per_night),
                    ("SPECIAL REQUEST", special_request),
                ],
            ),
            (
                f"Hi Ascot Hotel,\n"
                f"I want to book a {room_type} for two nights on {checkin_date} and {checkout_date}. "
                f"{special_request}\n"
                f"I have a promo code ({promo_code}). Is the price still {price_per_night} per night with breakfast included?\n"
                f"Let me know if you need more details.\n"
                f"Regards,\n"
                f"{guest_name}",
                [
                    ("GUEST", guest_name),
                    ("ROOM TYPE", room_type),
                    ("CHECKIN DATE", checkin_date),
                    ("CHECKOUT DATE", checkout_date),
                    ("PROMOTIONAL CODE", promo_code),
                    ("PRICE PER NIGHT", price_per_night),
                    ("SPECIAL REQUEST", special_request),
                ],
            ),
            (
                f"Hello,\n"
                f"I am interested in booking a {room_type} for two nights from {checkin_date} to {checkout_date}. "
                f"{special_request}\n"
                f"My promo code is ({promo_code}), and I believe the cost is {price_per_night} per night. Please confirm.\n"
                f"Kind regards,\n"
                f"{guest_name}",
                [
                    ("GUEST", guest_name),
                    ("ROOM TYPE", room_type),
                    ("CHECKIN DATE", checkin_date),
                    ("CHECKOUT DATE", checkout_date),
                    ("PROMOTIONAL CODE", promo_code),
                    ("PRICE PER NIGHT", price_per_night),
                    ("SPECIAL REQUEST", special_request),
                ],
            ),
            (
                f"Dear Ascot Hotel,\n"
                f"I’d like to book a {room_type} for two nights with breakfast. My stay is from {checkin_date} to {checkout_date}. "
                f"{special_request}\n"
                f"My promotional code is ({promo_code}). Is the total {price_per_night} per night?\n"
                f"Looking forward to your confirmation.\n"
                f"Warm regards,\n"
                f"{guest_name}",
                [
                    ("GUEST", guest_name),
                    ("ROOM TYPE", room_type),
                    ("CHECKIN DATE", checkin_date),
                    ("CHECKOUT DATE", checkout_date),
                    ("PROMOTIONAL CODE", promo_code),
                    ("PRICE PER NIGHT", price_per_night),
                    ("SPECIAL REQUEST", special_request),
                ],
            ),

        ]

        selected_template, applicable_entities = random.choice(templates_with_entities)
        text = selected_template

        # Ensure alignment for applicable entities
        entities = []
        for label, value in applicable_entities:
            start = text.find(str(value))
            end = start + len(str(value))
            entities.append((start, end, label))

        # Add text and entities to training data
        training_data.append((text, {"entities": entities}))
    return training_data

# Save the generated NER training data
def save_ner_training_data(training_data, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(training_data, f, ensure_ascii=False, indent=4)


# Generate and save NER training data
if __name__ == "__main__":
    num_examples =2000  # Adjust the number of training examples
    ner_training_data = generate_ner_training_data(num_examples)
    output_file_path = "generated_training_data.json"
    save_ner_training_data(ner_training_data, output_file_path)
    print(f"Generated {num_examples} NER training examples and saved to {output_file_path}.")
