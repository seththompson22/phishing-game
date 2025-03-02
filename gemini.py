from dataclasses import dataclass
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv
from random import randint as rint, sample as rsample

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))

def generate_email_with_gemini(user_name: str, sender_emails: list[str], num_senders: int, acceptable_senders: list[str], model_name: str):
    """
    Generates {num_senders} email(s) using Google's Generative AI (Gemini).

    Args:
        user_name (str): The name of the user to personalize the email.
        acceptable_emails (list): A list of acceptable email addresses.
        model_name (str): The name of the Gemini model to use.

    Returns:
        str: A JSON string representing the generated email.
    """
    try:
        model = genai.GenerativeModel(model_name)
        prompt = f"""
            You are tasked with generating example emails for a cybersecurity awareness game that teaches users how to identify scam emails. The emails should include both **legitimate and suspicious** examples to help users learn to recognize cybersecurity threats.  

            ### Instructions:  
            - Generate **{num_senders}** email(s) that vary between suspicious and legitimate emails.  
            - Separate each email with the '|' character.  
            - Structure each email using the format:  

            **name|address|subject|body|grammar|spelling|time|links|is_phish**  

            ### Guidelines:  
            1. **Suspisious Emails:**  
            - Should contain common phishing tactics such as urgency, misleading sender addresses, and requests for sensitive information.  
            - Use placeholders like `[User Name]`, `[Amount]`, `[Merchant]`, and `[fake_link]` but replace them with **realistic** values.  
            2. **Legitimate Emails:**  
            - Should resemble normal, professional communication without deceptive elements.  
            3. **Important**
            - at the end of each email say that this is for educational purposes only
            4. Increase length of the emails to 3-4 sentences. Fill in the user name with {user_name} and the sender email with the according {acceptable_senders} based on the {sender_emails}

            ### Examples:  
            IT Support|it@company.com|Password Reset Required|Dear User, reset here: fake-reset.com|high|high|any|suspicious|true  
            HR Department|hr@company.com|Meeting Reminder|Hello team, meeting at 10 AM Room 305.|high|high|any|non_suspicious|false  

            ### Context:  
            - User Name: {user_name}  
            - Acceptable Emails: {acceptable_senders}  
            - Ensure a mix of **realistic phishing and non-phishing** emails for training purposes. 
            - if the second value in the tuple within {sender_emails} is "phishing", then make a **realistic non-phishing email**, otherwise make a **realistic phishing email**,
            - Use the following sender emails: {sender_emails}, and fill in the information you generate in brackets with realistic values.
            """


        response = model.generate_content(prompt)
        print("gemini.py has run successfully")
        return response.text

    except Exception as e:
        print(f"Error: {e}")
        return None

