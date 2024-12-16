from flask import Flask, request, jsonify
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email_validator import validate_email, EmailNotValidError
from module import send_to_llm,guess_lang
import json
from datetime import datetime
app = Flask(__name__)


@app.route('/read-email', methods=['POST']) 
def read_email():
    
    try:
        request_data = request.get_json()  # Decode the request body
        message = request_data.get('payload')["message"]
        email_address = request_data.get('payload')["email_address"]
        subject = request_data.get('payload')["subject"]
        date_time  = datetime.strptime(request_data.get('payload')["date"], '%m/%d/%Y %H:%M:%S')
        
        date = f"{date_time.year}/{date_time.month}/{date_time.day}"
        time = f"{date_time.hour}:{date_time.minute}"
        

        # Validate required fields
        if not all([message, email_address, subject, date, time]):
            return jsonify({"error": "All fields (message, email_address, subject, date, time) are required."}), 400
        
        # Validate email address
        try:
            validate_email(email_address)
        except EmailNotValidError as e:
            return jsonify({"error": str(e)}), 400
        
        guess_language =guess_lang.guess_language_with_highest_probability(message)
        
        if guess_language !=None:
            response = send_to_llm.send_to_llm(message,guess_language,date)
        return jsonify({"success": True, "message":response}), 200

    except Exception as e:
        return jsonify({"error": str(e.with_traceback)}), 500
    


if __name__ == '__main__':
    app.run(debug=True, port=5000)
