import spacy
from spacy.training.example import Example
from spacy.tokens import DocBin
import json


def load_training_data(file_path):
    """Load training data from a JSON file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


# Step 2: Initialize or Load the Model
def create_blank_model(train_data):
    """Create a blank SpaCy model and add labels from the training data."""
    nlp = spacy.blank("en")  # Create a blank English model
    ner = nlp.add_pipe("ner")  # Add the NER pipeline
    # Add labels to the NER model
    for _, annotations in train_data:
        for ent in annotations["entities"]:
            ner.add_label(ent[2])
    return nlp

# Step 3: Train the Model
def train_model(nlp, train_data, n_iter=20):
    """Train the NER model."""
    optimizer = nlp.begin_training()
    for i in range(n_iter):
        losses = {}
        for text, annotations in train_data:
            example = Example.from_dict(nlp.make_doc(text), annotations)
            nlp.update([example], drop=0.5, losses=losses)
        print(f"Iteration {i+1}, Losses: {losses}")
    return nlp

# Step 4: Save the Model
def save_model(nlp, output_dir):
    """Save the trained model to disk."""
    nlp.to_disk(output_dir)
    print(f"Model saved to {output_dir}")

# Main Program
if __name__ == "__main__":
    # Path to training data
    training_data_file = "generated_training_data.json"

    # Load the training data
    TRAIN_DATA = load_training_data(training_data_file)

    # Create a blank model
    nlp = create_blank_model(TRAIN_DATA)

    # Train the model
    trained_nlp = train_model(nlp, TRAIN_DATA)

    # Save the model
    output_directory = "trained_ner_model"
    save_model(trained_nlp, output_directory)
