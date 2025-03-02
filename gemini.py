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

            ## Examples: 
                IT Support|it@company.com|Password Reset Required|Dear User, reset here: fake-reset.com|high|high|any|suspicious|true 
                HR Department|hr@company.com|Meeting Reminder|Hello team, meeting at 10 AM Room 305.|high|high|any|non_suspicious|false
                Wells Fargo|alerts@wellsfargo.com|Account Alert|Your account has unusual activity. Click here: fake-wellsfargo.com|high|high|wellsfargo.com|suspicious|true
                Carl Weezer|weezing@carl.com|Party Invite|Hey dude, party at my place!|low|low|carl.com|non_suspicious|false
                Amazon Orders|order-update@amazon.com|Order Confirmation|Your order #12345 has shipped.|medium|high|amazon.com|non_suspicious|false
                LinkedIn Notifications|notifications-noreply@linkedin.com|New Connection|You have a new connection request.|medium|medium|linkedin.com|non_suspicious|false
                GitHub Updates|noreply@github.com|Pull Request Update|PR #567 has been merged.|medium|medium|github.com|non_suspicious|false
                Netflix Account|account@netflix.com|Account Payment|Your payment was successful.|high|high|netflix.com|non_suspicious|false
                Spotify Listeners|noreply@spotify.com|New Playlist|Check out this new playlist!|low|medium|spotify.com|non_suspicious|false
                Google Account|security-alert@accounts.google.com|Security Alert|Suspicious login detected.|high|high|google.com|suspicious|true
                Apple ID|appleid@id.apple.com|Password Reset|Your Apple ID password reset request.|high|high|apple.com|suspicious|true
                Microsoft Account|account-security-noreply@accountprotection.microsoft.com|Security Code|Your security code is 123456.|high|high|microsoft.com|non_suspicious|false
                Facebook Notifications|notification@facebookmail.com|Friend Request|You have a new friend request.|low|medium|facebookmail.com|non_suspicious|false
                Twitter (X) Updates|noreply@mail.x.com|New Follower|You have a new follower.|low|medium|x.com|non_suspicious|false
                Instagram Updates|mail@instagram.com|Direct Message|You have a new direct message.|low|medium|instagram.com|non_suspicious|false
                Paypal Transactions|service@paypal.com|Transaction Confirmation|Your payment to Example Merchant was successful.|high|high|paypal.com|non_suspicious|false
                Ebay Purchases|ebay@ebay.com|Item Shipped|Your item has shipped.|medium|high|ebay.com|non_suspicious|false
                Zoom Meetings|no-reply@zoom.us|Meeting Invitation|You are invited to a Zoom meeting.|medium|medium|zoom.us|non_suspicious|false
                Slack Notifications|notifications@slack.com|New Message|You have a new message in #general.|medium|medium|slack.com|non_suspicious|false
                Handshake Notifications|notifications@joinhandshake.com|Job Posting|New job posting matching your interests.|medium|medium|joinhandshake.com|non_suspicious|false
                LinkedIn Messages|messages-noreply@linkedin.com|New Message|You have a new message.|medium|medium|linkedin.com|non_suspicious|false
                Walmart Grocery|orders@walmartgrocery.com|Order Confirmation|Your grocery order is confirmed.|medium|high|walmartgrocery.com|non_suspicious|false
                Kroger Grocery|myaccount@kroger.com|Account Update|Your Kroger account was updated.|medium|high|kroger.com|non_suspicious|false
                Aldi Grocery|feedback@aldi.us|Survey Invitation|Please take our customer survey.|low|medium|aldi.us|non_suspicious|false
                Target Grocery|order@target.com|Order Ready|Your Target grocery order is ready for pickup.|medium|high|target.com|non_suspicious|false
                Instacart|support@instacart.com|Support Ticket|Your support ticket has been updated.|medium|medium|instacart.com|non_suspicious|false
                Whole Foods Market|orders@wholefoodsmarket.com|Order Confirmation|Your Whole Foods order is confirmed.|medium|high|wholefoodsmarket.com|non_suspicious|false
                Trader Joe's|noreply@traderjoes.com|Weekly Flyer|Check out this week's specials!|low|low|traderjoes.com|non_suspicious|false
                Local Grocery Store|orders@localgrocerystore.com|Order Confirmation|Your order is confirmed.|medium|high|localgrocerystore.com|non_suspicious|false

            ### Context:  
            - User Name: {user_name}  
            - Acceptable Emails: {acceptable_senders}  
            - Ensure a mix of **realistic phishing and non-phishing** emails for training purposes. 
            - if the second value in the tuple within {sender_emails} is "phishing", then make a **realistic non-phishing email**, otherwise make a **realistic phishing email**,
            - Use the following sender emails: {sender_emails}, and fill in the information you generate in brackets with realistic values. keep to a similar format to what i gave you.
            """


        response = model.generate_content(prompt)
        print("gemini.py has run successfully")
        return response.text

    except Exception as e:
        print(f"Error: {e}")
        return None

