import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))

def generate_email_with_gemini(user_name, acceptable_emails, model_name):
    """
    Generates a phishing email using Google's Generative AI (Gemini).

    Args:
        user_name (str): The name of the user to personalize the email.
        acceptable_emails (list): A list of acceptable email addresses.
        model_name (str): The name of the Gemini model to use.

    Returns:
        str: A JSON string representing the generated email.
    """
    try:
        # Initialize the Gemini model
        model = genai.GenerativeModel(model_name)

        # Create the prompt for the model
        prompt = f"""
        Generate a phishing email in JSON format with the following structure:
        {{
          "name": "Sender Name",
          "address": "sender@example.com",
          "subject": "Email Subject",
          "body": "Email Body",
          "checks": {{
            "grammar": "high" or "low",
            "spelling": "high" or "low",
            "time": "any",
            "links": "suspicious" or "non_suspicious"
          }},
          "is_phish": true or false
        }}

        Use the following details:
        - User Name: {user_name}
        - Acceptable Emails: {acceptable_emails}
        - Replace placeholders like [User Name], [Amount], [Merchant], and [fake_link] with realistic values.

        Examples:
        [
            {{
                "name": "IT",
                "address": "it@co.net",
                "subject": "Reset Password",
                "body": "Dear {user_name}, please reset your password here: fake.com",
                "checks": {{
                    "grammar": "low",
                    "spelling": "high",
                    "time": "any",
                    "links": "suspicious"
                }},
                "is_phish": true
            }},
            {{
                "name": "HR",
                "address": "hr@co.com",
                "subject": "Meeting Reminder",
                "body": "Team, we have a meeting at 10 AM.",
                "checks": {{
                    "grammar": "high",
                    "spelling": "high",
                    "time": "any",
                    "links": "non_suspicious"
                }},
                "is_phish": false
            }}
        ]
        """

        # Generate the email using the model
        response = model.generate_content(prompt)

        # Return the raw response text
        return response.text

    except Exception as e:
        print(f"Error generating email with model {model_name}: {e}")
        return None