import spacy
from spacy.tokens import DocBin
import json

def convert_to_spacy_format(input_file, output_file):
    nlp = spacy.blank("en")  # Use the appropriate language code for your data
    doc_bin = DocBin()
    
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    for entry in data:
        text = entry[0]
        annotations = entry[1]
        entities = annotations.get("entities", [])
        
        doc = nlp.make_doc(text)
        ents = []
        for start, end, label in entities:
            span = doc.char_span(start, end, label=label, alignment_mode="contract")
            if span is None:
                print(f"Skipping entity: {text[start:end]} in text: {text}")
                continue
            ents.append(span)
        
        doc.ents = ents
        doc_bin.add(doc)
    
    doc_bin.to_disk(output_file)
    print(f"Saved to {output_file}")

# Convert your data to spaCy format
convert_to_spacy_format("generated_training_data.json", "train.spacy")
