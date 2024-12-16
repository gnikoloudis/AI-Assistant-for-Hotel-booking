import os
from openai import OpenAI

# Replace with your OpenAI API key
client =OpenAI(api_key = "")

def generate_variations(prompt, num_variations=5):
    """
    Generate diverse variations for a given prompt using OpenAI API.
    """
    variations = []
    for _ in range(num_variations):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                        {"role": "system", "content": "You are a generator of email variations."},
                        {
                            "role": "user",
                            "content": prompt
                        }
            ]
        )
        variations.append(response.choices[0].message.content.strip())
    return variations

def create_email_variations(input_directory, output_directory, num_variations=5):
    """
    Reads emails from the input directory, generates variations for each,
    and saves the variations in the output directory.

    Parameters:
        input_directory (str): Path to the directory containing email files.
        output_directory (str): Path to save the generated variations.
        num_variations (int): Number of variations to generate per email.
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(input_directory):
        if filename.endswith(".txt"):
            # Read the email content
            input_file_path = os.path.join(input_directory, filename)
            with open(input_file_path, "r", encoding="utf-8") as file:
                base_email = file.read().strip()

            # Generate variations
            prompt = f"Create diverse variations of the following email while keeping its meaning intact:\n\n{base_email}"
            variations = generate_variations(prompt, num_variations=num_variations)

            # Save variations to a new file
            output_file_path = os.path.join(output_directory, f"variations_{filename}")
            with open(output_file_path, "w", encoding="utf-8") as output_file:
                for idx, variation in enumerate(variations, start=1):
                    output_file.write(f"Variation {idx}:\n{variation}\n\n")

            print(f"Variations for {filename} saved to {output_file_path}")

# Define the directories
input_directory = "emails"  # Directory containing input email files
output_directory = "email_variations"  # Directory to save the variations

# Generate variations for all emails
create_email_variations(input_directory, output_directory, num_variations=2)
