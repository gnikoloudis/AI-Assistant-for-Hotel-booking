import logging

# Create a custom logger
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)

# Create handlers
console_handler = logging.StreamHandler()  # Logs to console
file_handler = logging.FileHandler('app.log')  # Logs to file

# Set levels for handlers
console_handler.setLevel(logging.WARNING)  # Only log warnings and above to console
file_handler.setLevel(logging.DEBUG)  # Log all levels to file

# Create a formatter and set it for both handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
