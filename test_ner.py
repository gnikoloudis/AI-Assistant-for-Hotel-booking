import spacy
import pandas as pd
import json

# Function to load JSON file with emails
def load_emails(file_path):
    """Load email texts from a JSON file."""
    with open(file_path, "r", encoding="utf-8") as file:
        emails = json.load(file)
    return emails

# Function to extract entities using a SpaCy model
def extract_entities_from_emails(nlp, emails):
    """Extract entities from emails and organize them into a structured format."""
    results = []
    for email in emails:
        doc = nlp(email)
        extracted_entities = {
            "Email": email,
            "GUEST": [],
            "ROOM TYPE": [],
            "NUMBER OF GUESTS": [],
            "GUEST TYPE": [],
            "CHECKIN DATE": [],
            "CHECKOUT DATE": [],
        }
        for ent in doc.ents:
            if ent.label_ in extracted_entities:
                extracted_entities[ent.label_].append(ent.text)
        # Flatten lists where applicable
        for key in extracted_entities:
            if key != "Email":
                extracted_entities[key] = ", ".join(extracted_entities[key])
        results.append(extracted_entities)
    return results

# Function to create a DataFrame
def create_dataframe(entities):
    """Convert extracted entities into a Pandas DataFrame."""
    return pd.DataFrame(entities)

# Main program
if __name__ == "__main__":
    # Path to the JSON file containing emails
    email_file_path = "test_data.json"  # Replace with your JSON file path

    # Path to the trained SpaCy model
    trained_model_path = "trained_ner_model"  # Replace with your trained model directory

    # Load emails
    emails = load_emails(email_file_path)

    # Load the trained SpaCy model
    nlp = spacy.load(trained_model_path)

    # Extract entities from emails
    entities = extract_entities_from_emails(nlp, emails)

    # Create a DataFrame
    df = create_dataframe(entities)
