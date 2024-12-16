from langdetect import detect, detect_langs
from module import app_logging

def guess_language_with_highest_probability(message):
    try:
        possible_langs = detect_langs(message)  # List of languages with probabilities
        best_lang = max(possible_langs, key=lambda x: x.prob)  # Get the language with the highest probability
        
        return best_lang.lang
    except Exception as e:
        app_logging.error(f"Error in language detection: {e.with_traceback}")